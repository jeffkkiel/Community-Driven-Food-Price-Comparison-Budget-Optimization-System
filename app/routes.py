
import os
from uuid import uuid4
from decimal import Decimal

from datetime import datetime, timezone, timedelta

from flask import render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
import sqlalchemy as sa

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from app import app, db
from app.forms import *
from app.models import *
from app.services.helper import time_ago


@app.route("/", methods=["GET", "POST"])
def dashboard():
    comprForm = CompareForm()

    manila = timezone(timedelta(hours=8))
    start_of_day = (
        datetime.now(manila)
        .replace(hour=0, minute=0, second=0, microsecond=0)
        .astimezone(timezone.utc)
    )

    stats = {
        "stores": db.session.scalar(db.select(func.count(Store.id))),
        "foods": db.session.scalar(db.select(func.count(Product.id))),
        "locations": db.session.scalar(db.select(func.count(func.distinct(Store.location)))),
        "today": db.session.scalar(db.select(func.count(PriceHistory.id)).where(PriceHistory.recorded_at >= start_of_day)),
    }

    recent = db.session.execute(
        db.select(PriceHistory, Product, Store)
        .join(ProductStore, PriceHistory.product_store_id == ProductStore.id)
        .join(Product, ProductStore.product_id == Product.id)
        .join(Store, ProductStore.store_id == Store.id)
        .order_by(PriceHistory.recorded_at.desc())
        .limit(5)
    ).all()

    activity = [
        {
            "food": product.name,
            "price": history.price,
            "store": store.name,
            "location": store.location,
            "time": time_ago(history.recorded_at),
        }
        for history, product, store in recent
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

    # para sa dropdown(chat for explanation)
    stores = db.session.scalars(
        db.select(Store).order_by(Store.name, Store.location)
    ).all()

    form.store.choices = [
        ("", "Choose a store"),
        *[
            (str(store.id), f"{store.name} — {store.location}")
            for store in stores
        ],
        ("__new__", "Add a new store..."),
    ]

    if form.validate_on_submit():
        if form.category.data not in CATEGORIES:
            flash("Please choose a valid category.")
            return render_template("add_product.html", form=form)

        if form.location.data not in LOCATIONS:
            flash("Please choose a valid location.")
            return render_template("add_product.html", form=form)

        store = None

        # let user choose existing store or make new one
        if form.store.data == "__new__":
            store_name = (form.store_name.data or "").strip()

            if not store_name:
                form.store_name.errors.append(
                    "Enter a name for the new store."
                )
                return render_template("add_product.html", form=form)

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

        else:
            # chcik if the selected store actually exists.
            try:
                store_id = int(form.store.data)
            except (ValueError, TypeError):
                flash("Please select a valid store.")
                return render_template("add_product.html", form=form)

            store = db.session.get(Store, store_id)

            if store is None:
                flash("The selected store does not exist.")
                return render_template("add_product.html", form=form)

            if store.location != form.location.data:
                flash("The selected store and location do not match.")
                return render_template("add_product.html", form=form)

        try:
            product_name = form.product.data.strip()

            # reuse existing product with the same name.
            product = db.session.scalar(
                db.select(Product).where(
                    func.lower(Product.name) == product_name.lower()
                )
            )

            if product is None:
                product = Product(
                    name=product_name,
                    description=form.description.data or None,
                    category=form.category.data,
                )
                db.session.add(product)
                db.session.flush()

            # save optional uploaded image. idk pwede tanggalin kung medyo idk
            image = form.img.data

            if image and image.filename:
                safe_name = secure_filename(image.filename)

                if not safe_name:
                    raise ValueError(
                        "Please upload a valid image filename."
                    )

                filename = f"{uuid4().hex}_{safe_name}"
                upload_dir = os.path.join(app.static_folder, "uploads")
                os.makedirs(upload_dir, exist_ok=True)

                image.save(os.path.join(upload_dir, filename))
                product.img_ref = f"uploads/{filename}"

            # check if product already exists for price history
            listing = db.session.scalar(
                db.select(ProductStore).where(
                    ProductStore.product_id == product.id,
                    ProductStore.store_id == store.id,
                )
            )

            quantity = form.quantity.data
            total_price = form.total_price.data
            price = total_price / quantity

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

            # record price
            history = PriceHistory(
                product_store=listing,
                price=price,
            )
            db.session.add(history)

            db.session.commit()

        except (SQLAlchemyError, OSError, ValueError):
            db.session.rollback()
            app.logger.exception("Failed to add product and price")
            flash("Could not save the product. Please try again.")
            return render_template("add_product.html", form=form)

        flash("Product and price saved successfully.")
        return redirect(url_for("dashboard"))

    if form.is_submitted():
        print(form.errors)

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
