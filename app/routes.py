from datetime import datetime, timezone, timedelta, date, time as dtime
from app.services.search import search_prices

from flask import render_template, flash, redirect, url_for, request, session
import sqlalchemy as sa

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from app import app, db
from app.forms import *
from app.models import *
from app.services.helper import time_ago, format_number
from app.services.add_product import setup_product_form, validate_category_location, save_product_submission

from sqlalchemy.exc import SQLAlchemyError




@app.route("/", methods=["GET", "POST"])
def dashboard():
    form = CompareForm()
    products = db.session.scalars(
        db.select(Product).order_by(Product.name)).all()
    form.product.choices = [(str(prod.id), prod.name) for prod in products]
    selected_ids = session.get('compare_products', [])

    if form.validate_on_submit():
        product_id = form.product.data
        if product_id not in selected_ids:
            selected_ids.append(product_id)
        session['compare_products'] = selected_ids
        return redirect(url_for('dashboard'))

    selected_products = db.session.scalars(db.select(Product).where(
        Product.id.in_(selected_ids))).all() if selected_ids else []

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
            "price": format_number(history.price),
            "store": store.name,
            "location": store.location,
            "time": time_ago(history.recorded_at),
        }
        for history, product, store in recent
    ]

    q = request.args.get("q", "").strip()
    groups = search_prices(q) if q else None

    return render_template(
        "dashboard.html",
        form=form,
        stats=stats,
        activity=activity,
        selected_products=selected_products,
        q=q,
        groups=groups,
    )


@app.route("/add", methods=["GET", "POST"])
def add_product():
    form = ProductForm()
    setup_product_form(form)

    if form.validate_on_submit():
        error = validate_category_location(form)

        if error:
            flash(error)
            return render_template("add_product.html", form=form)

        try:
            saved = save_product_submission(form)

            if not saved:
                return render_template("add_product.html", form=form)

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

@app.route("/compare", methods=["GET", "POST"])
def compare():
    form = CompareForm
    return render_template("compare.html", form=form)

@app.route("/day-summary")
def day_summary():
    manila = timezone(timedelta(hours=8))
    today = datetime.now(manila).date()

    try:
        chosen = date.fromisoformat(request.args.get("date", ""))
        if chosen > today:
            chosen = today

    except ValueError:
        chosen = today

    start = datetime.combine(
        chosen, dtime.min, tzinfo=manila).astimezone(timezone.utc)
    end = start + timedelta(days=1)

    rows = db.session.execute(
        db.select(PriceHistory, Product, Store)
        .join(ProductStore, PriceHistory.product_store_id == ProductStore.id)
        .join(Product, ProductStore.product_id == Product.id)
        .join(Store, ProductStore.store_id == Store.id)
        .where(
            PriceHistory.recorded_at >= start,
            PriceHistory.recorded_at < end
        )
        .order_by(PriceHistory.recorded_at.desc())
    ).all()

    entries = []

    for history, product, store in rows:
        recorded = history.recorded_at

        if recorded.tzinfo is None:
            recorded = recorded.replace(tzinfo=timezone.utc)

        entries.append({
            "time": recorded.astimezone(manila).strftime("%I:%M %p"),
            "food": product.name,
            "category": product.category,
            "store": store.name,
            "location": store.location,
            "price": history.price
        })
    return render_template("day_summary.html", chosen=chosen, today=today, entries=entries)
