from datetime import timezone, timedelta

import sqlalchemy as sa

from app import db
from app.models import Product, Store, ProductStore, PriceHistory

MANILA = timezone(timedelta(hours=8))


def search_prices(q):
    safe = q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")

    latest = (
        db.select(PriceHistory.product_store_id, sa.func.max(
            PriceHistory.recorded_at).label("last"),)
        .group_by(PriceHistory.product_store_id)
        .subquery()
    )

    rows = db.session.execute(
        db.select(ProductStore, Product, Store, latest.c.last)
        .join(Product, ProductStore.product_id == Product.id)
        .join(Store, ProductStore.store_id == Store.id)
        .join(latest, latest.c.product_store_id == ProductStore.id)
        .where(Product.name.ilike(f"%{safe}%", escape="\\"))
        .order_by(Store.location, Product.name, ProductStore.price)
    ).all()

    groups = {}
    for listing, product, store, last in rows:
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)

        groups.setdefault(store.location, []).append({
            "food": product.name,
            "store": store.name,
            "price": listing.price,
            "date": last.astimezone(MANILA).strftime("%b %d, %Y"),
        })

    return groups
