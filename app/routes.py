import os
from uuid import uuid4
from decimal import Decimal

from flask import render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
import sqlalchemy as sa

from app import app, db
from app.forms import *
from app.models import *


@app.route("/", methods=["GET", "POST"])
def dashboard():
    comprForm = CompareForm()
    stats = {"stores": 0, "foods": 0, "users": 0, "prices": 0}
    activity = [
        {"username": "Ian", "food": "Jeff",
            "location": "Justin", "time": "0 hr ago"},
    ]
    return render_template(
        "dashboard.html",
        comprForm=comprForm,
        stats=stats,
        activity=activity,
    )


@app.route("/add", methods=["GET", "POST"])
def add_product():
    form = ProductForm()

    # Populate dynamic dropdown choices here.
    stores = db.session.scalars(db.select(Store).order_by(Store.name, Store.location)).all()
    form.store.choices = [("", "Choose a store"), *[(str(store.id), f"{store.name} — {store.location}") for store in stores],
            ("__new__", "Add a new store..."),]

    if form.validate_on_submit():
        if form.category.data not in CATEGORIES:
            flash("Please choose a valid category.")
            return render_template("add_product.html", form=form)
        if form.address.data not in LOCATIONS:
            flash("Please choose a valid location.")
            return render_template("add_product.html", form=form)

        store = None

        #let user choose existing store or make new one
        if form.store.data == "__new__":
            store_name = (form.store_name.data or "").strip()
            if not store_name:
                form.store_name.errors.append("Enter a name for the new store.")
                return render_template("add_product.html", form=form)

            store = db.session.scalar(
                db.select(Store).where(
                    func.lower(Store.name) == store_name.lower(),
                    Store.location == form.address.data,))

            if store is None:
                store = Store(name=store_name, location=form.address.data,)
                db.session.add(store)
                db.session.flush()

        else:
            # Verify the selected store actually exists.
            try:
                store_id = int(form.store.data)
            except (ValueError, TypeError):
                flash("Please select a valid store.")
                return render_template("add_product.html", form=form)

            store = db.session.get(Store, store_id)

            if store is None:
                flash("The selected store does not exist.")
                return render_template("add_product.html", form=form)

            if store.location != form.address.data:
                flash("The selected store and location do not match.")
                return render_template("add_product.html", form=form)
        try:
            product_name = form.product.data.strip()

            # Reuse an existing product with the same name.
            product = db.session.scalar(db.select(Product).where(func.lower(Product.name) == product_name.lower()))

            if product is None:
                product = Product(
                    name=product_name,
                    description=form.description.data or None,
                    category=form.category.data,
                )
                db.session.add(product)
                db.session.flush()

            # Save an optional uploaded image.
            image = form.img.data
            if image and image.filename:
                safe_name = secure_filename(image.filename)

                if not safe_name:
                    raise ValueError("Please upload a valid image filename.")

                filename = f"{uuid4().hex}_{safe_name}"
                upload_dir = os.path.join(app.static_folder, "uploads")
                os.makedirs(upload_dir, exist_ok=True)

                image.save(os.path.join(upload_dir, filename))
                product.img_ref = f"uploads/{filename}"

            # Find an existing listing for this product and store.
            listing = db.session.scalar(
                db.select(ProductStore).where(ProductStore.product_id == product.id, ProductStore.store_id == store.id,))

            price = form.price.data

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

            # Record every submitted price as a historical observation.
            history = PriceHistory(product_store=listing,price=price,)
            db.session.add(history)

            db.session.commit()

        except (SQLAlchemyError, OSError, ValueError):
            db.session.rollback()
            app.logger.exception("Failed to add product and price")
            flash("Could not save the product. Please try again.")
            return render_template("add_product.html", form=form)

        flash("Product and price saved successfully.")
        return redirect(url_for("dashboard"))

    return render_template("add_product.html", form=form)
    


@app.route("/optimize")
def optimize():
    return render_template("optimize.html")


@app.route("/contributions")
def contributions():
    return render_template("contributions.html")


@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/day-summary")
def day_summary():
    return render_template("day_summary.html")
