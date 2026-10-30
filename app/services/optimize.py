from decimal import Decimal

from app import db
from app.models import Product, ProductStore, Store

CENT = Decimal("0.01")


def get_locations():
    """Return only locations that have at least one product listing."""
    return db.session.scalars(
        db.select(Store.location)
        .join(ProductStore, ProductStore.store_id == Store.id)
        .distinct()
        .order_by(Store.location)
    ).all()


def get_location_stores(location):
    """Return the stores in a location that have at least one listing."""
    return db.session.scalars(
        db.select(Store.name)
        .join(ProductStore, ProductStore.store_id == Store.id)
        .where(Store.location == location)
        .distinct()
        .order_by(Store.name)
    ).all()


def _cheapest(current, listing, product, store):
    if current is None or (listing.price, store.name) < (
        current["price"],
        current["store"].name,
    ):
        return {
            "product": product,
            "store": store,
            "price": listing.price,
        }

    return current


def get_location_products(location):
    """Return one row per product: its cheapest listing in the location."""
    rows = db.session.execute(
        db.select(ProductStore, Product, Store)
        .join(Product, ProductStore.product_id == Product.id)
        .join(Store, ProductStore.store_id == Store.id)
        .where(Store.location == location)
    ).all()

    cheapest = {}
    for listing, product, store in rows:
        cheapest[product.id] = _cheapest(
            cheapest.get(product.id), listing, product, store
        )

    return sorted(
        cheapest.values(),
        key=lambda row: (row["product"].category, row["product"].name),
    )


def get_product_categories(products):
    """Return the sorted category names present in a product row list."""
    return sorted({row["product"].category for row in products})


def calculate_plan(location, budget, quantities):
    """Price a fixed basket using the cheapest store per item in one location."""
    product_ids = list(quantities)

    products = {
        product.id: product
        for product in db.session.scalars(
            db.select(Product).where(Product.id.in_(product_ids))
        )
    }

    rows = db.session.execute(
        db.select(ProductStore, Product, Store)
        .join(Product, ProductStore.product_id == Product.id)
        .join(Store, ProductStore.store_id == Store.id)
        .where(Store.location == location, Product.id.in_(product_ids))
    ).all()

    cheapest = {}
    store_prices = {}

    for listing, product, store in rows:
        cheapest[product.id] = _cheapest(
            cheapest.get(product.id), listing, product, store
        )

        store_data = store_prices.setdefault(
            store.id, {"store": store, "prices": {}}
        )
        old_price = store_data["prices"].get(product.id)
        if old_price is None or listing.price < old_price:
            store_data["prices"][product.id] = listing.price

    items = []
    missing = []
    total = Decimal("0.00")

    for product_id, quantity in quantities.items():
        best = cheapest.get(product_id)

        if best is None:
            product = products.get(product_id)
            missing.append(product.name if product else f"Product #{product_id}")
            continue

        subtotal = (best["price"] * quantity).quantize(CENT)
        total += subtotal
        items.append({
            "product": best["product"],
            "quantity": quantity,
            "store": best["store"],
            "unit_price": best["price"],
            "subtotal": subtotal,
        })

    items.sort(key=lambda item: (item["product"].category, item["product"].name))

    store_totals = []
    for store_data in store_prices.values():
        store_total = Decimal("0.00")
        missing_items = []
        store_lines = []

        for product_id, quantity in quantities.items():
            price = store_data["prices"].get(product_id)
            product = products.get(product_id)

            if price is None:
                missing_items.append(
                    product.name if product else f"Product #{product_id}"
                )
                continue

            subtotal = (price * quantity).quantize(CENT)
            store_total += subtotal
            store_lines.append({
                "product": product,
                "quantity": quantity,
                "unit_price": price,
                "subtotal": subtotal,
                "is_best": (
                    store_data["store"].id == cheapest[product_id]["store"].id
                    and price == cheapest[product_id]["price"]
                ),
            })

        store_lines.sort(
            key=lambda line: (line["product"].category, line["product"].name)
        )

        store_totals.append({
            "store": store_data["store"],
            "lines": store_lines,
            "total": store_total,
            "covered": len(quantities) - len(missing_items),
            "needed": len(quantities),
            "missing": missing_items,
            "complete": not missing_items,
        })

    store_totals.sort(
        key=lambda row: (not row["complete"], row["total"], row["store"].name)
    )

    cheapest_store = next((row for row in store_totals if row["complete"]), None)
    total = total.quantize(CENT)
    remaining = (budget - total).quantize(CENT)
    savings = None

    if cheapest_store is not None:
        savings = max(
            Decimal("0.00"),
            (cheapest_store["total"] - total).quantize(CENT),
        )

    return {
        "lines": items,
        "missing": missing,
        "total": total,
        "budget": budget.quantize(CENT),
        "remaining": remaining,
        "store_totals": store_totals,
        "cheapest_store": cheapest_store,
        "savings": savings,
    }
