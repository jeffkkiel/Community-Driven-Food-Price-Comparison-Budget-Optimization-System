
import os
from uuid import uuid4

from werkzeug.utils import secure_filename
from sqlalchemy import func

from app import app, db
from app.models import Product, Store, ProductStore, PriceHistory


def validate_category_location(form):
    #Validate the selected category and location.
    if form.category.data not in form.category.choices:
        return "Please choose a valid category."

    if form.location.data not in form.location.choices:
        return "Please choose a valid location."

    return None


def setup_product_form(form):
    #populate store and product dropdowns.
    stores = db.session.scalars(db.select(Store).order_by(Store.name, Store.location)).all()

    form.store.choices = [
        ("", "Choose a store"), ("__new__", "Add a new store..."),
        *[
            (str(store.id), f"{store.name} — {store.location}")
            for store in stores
        ],]

    products = db.session.scalars(db.select(Product).order_by(Product.name)).all()
    
    form.product.choices = [
        ("", "Choose a product"), ("__new__", "Add a new product..."),
        *[
            (str(product.id), f"{product.name}")
            for product in products
        ],]


def get_or_create_store(form):
    # let user choose existing store or make new one
    if form.store.data == "__new__":
        store_name = (form.store_name.data or "").strip()

        if not store_name:
            form.store_name.errors.append(
                "Enter a name for the new store."
            )
            return None

        store = db.session.scalar(
            db.select(Store).where(
                func.lower(Store.name) == store_name.lower(),
                Store.location == form.location.data,
            )
        )

        if store is None:
            store = Store(
                name=store_name,
                location=form.location.data,
            )
            db.session.add(store)
            db.session.flush()

        return store
    # chcik if the selected store actually exists.
    try:
        store_id = int(form.store.data)
    except (ValueError, TypeError):
        raise ValueError("Please select a valid store.")

    store = db.session.get(Store, store_id)

    if store is None:
        raise ValueError("The selected store does not exist.")

    if store.location != form.location.data:
        raise ValueError(
            "The selected store and location do not match."
        )

    return store


def get_or_create_product(form):
    # let user choose existing product or make new one
    if form.product.data == "__new__":
        product_name = (form.product_name.data or "").strip()

        if not product_name:
            form.product_name.errors.append(
                "Enter a name for the new product."
            )
            return None

        product = db.session.scalar(db.select(Product).where(func.lower(Product.name) == product_name.lower()))

        if product is None:
            product = Product(name=product_name, description=form.description.data or None, category=form.category.data)
            db.session.add(product)
            db.session.flush()

        return product
    # chcik if the selected store actually exists.
    try:
        product_id = int(form.product.data)
    except (ValueError, TypeError):
        raise ValueError("Please select a valid product.")

    product = db.session.get(Product, product_id)

    if product is None:
        raise ValueError("The selected product does not exist.")

    return product


def save_product_image(form, product):
    # save optional uploaded image. idk pwede tanggalin kung medyo idk
    image = form.img.data

    if not image or not image.filename:
        return

    safe_name = secure_filename(image.filename)

    if not safe_name:
        raise ValueError("Please upload a valid image filename.")

    filename = f"{uuid4().hex}_{safe_name}"
    upload_dir = os.path.join(app.static_folder, "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    image.save(os.path.join(upload_dir, filename))
    product.img_ref = f"uploads/{filename}"


def get_or_create_listing(product, store, price):
    # check if product already exists for price history
    listing = db.session.scalar(
        db.select(ProductStore).where(
            ProductStore.product_id == product.id,
            ProductStore.store_id == store.id,
        )
    )

    if listing is None:
        listing = ProductStore(
            product=product,
            store=store,
            price=price,
        )
        db.session.add(listing)
        db.session.flush()
    else:
        listing.price = price

    return listing


def record_price(listing, price):
    # record price
    history = PriceHistory(
        product_store=listing,
        price=price,
    )
    db.session.add(history)


def save_product_submission(form):
    #submit lahat sa db
    store = get_or_create_store(form)
    if store is None:
        return False
    product = get_or_create_product(form)
    if product is None:
        return False
    save_product_image(form, product)

    price = form.total_price.data / form.quantity.data
    listing = get_or_create_listing(product, store, price)
    record_price(listing, price)

    db.session.commit()
    return True