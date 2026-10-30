from datetime import datetime, timezone, timedelta, date, time as dtime
from decimal import Decimal, InvalidOperation

from app.services.optimize import (
    calculate_plan,
    get_location_products,
    get_location_stores,
    get_locations,
    get_product_categories,
)
from app.services.search import search_prices

from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

import os
from dotenv import load_dotenv
load_dotenv()

import urllib.request

from flask import render_template, flash, redirect, url_for, request, session
import sqlalchemy as sa

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app import app, db
from app.forms import *
from app.models import *
from app.services.helper import time_ago, format_number
from app.services.add_product import setup_product_form, validate_category_location, save_product_submission

from sqlalchemy.exc import SQLAlchemyError

# for perm website auto-update through /update route
import subprocess

@app.before_request
def require_login():
    allowed = ("login", "register", "static")
    if not current_user.is_authenticated and request.endpoint not in allowed:
        return redirect(url_for("login"))
    

@app.route("/login", methods=["GET", "POST"], endpoint="login")
@app.route("/register", methods=["GET", "POST"], endpoint="register")
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    mode = "register" if request.path == "/register" else "login"
    form = AuthForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        user = db.session.scalar(db.select(User).where(func.lower(User.username) == username.lower()))

        if mode == "register":
            if len(form.password.data) < 8:
                form.password.errors.append("Use at least 8 characters.")
            elif form.password.data != form.password2.data:
                form.password2.errors.append("Password do not match.")
            elif user:
                form.username.errors.append("That username is taken. Please try again.")
            else:
                user = User(username=username, password_hash=generate_password_hash(form.password.data))
                db.session.add(user)
                try:
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    form.username.errors.append("That username is taken. Please try again.")
                else:
                    login_user(user)
                    return redirect(url_for("dashboard"))
        else:
            if user is None or not check_password_hash(user.password_hash, form.password.data):
                flash("Wrong username or password.", "error")
            else:
                login_user(user)
                return redirect(url_for("dashboard"))

    return render_template("auth.html", form=form, mode=mode)


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
def dashboard():

    manila = timezone(timedelta(hours=8))
    start_of_day = (
        datetime.now(manila)
        .replace(hour=0, minute=0, second=0, microsecond=0)
        .astimezone(timezone.utc)
    )

    stats = {
        "stores": db.session.scalar(db.select(func.count(Store.id))),
        "foods": db.session.scalar(db.select(func.count(Product.id))),
        "users": db.session.scalar(db.select(func.count(User.id))),
        "today": db.session.scalar(db.select(func.count(PriceHistory.id)).where(PriceHistory.recorded_at >= start_of_day)),
    }

    recent = db.session.execute(
        db.select(PriceHistory, Product, Store, User)
        .join(ProductStore, PriceHistory.product_store_id == ProductStore.id)
        .join(Product, ProductStore.product_id == Product.id)
        .join(Store, ProductStore.store_id == Store.id)
        .outerjoin(User, PriceHistory.user_id == User.id)
        .order_by(PriceHistory.recorded_at.desc())
        .limit(3)
    ).all()

    activity = [
        {
            "user": user.username if user else "Anonymous",
            "food": product.name,
            "price": format_number(history.price),
            "store": store.name,
            "location": store.location,
            "time": time_ago(history.recorded_at),
        }
        for history, product, store, user in recent
    ]

    q = request.args.get("q", "").strip()
    groups = search_prices(q) if q else None

    return render_template(
        "dashboard.html",

        stats=stats,
        activity=activity,
        
        q=q,
        groups=groups,
    )         # form=form, # selected_products=selected_products,


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


@app.route("/optimize", methods=["GET", "POST"])
def optimize():
    locations = get_locations()
    form = OptimizeForm()
    form.location.choices = [("", "Choose a location")] + [
        (location, location) for location in locations
    ]

    if request.method == "POST" and request.form.get("step") == "calculate":
        location = request.form.get("location", "")
        budget_raw = request.form.get("budget", "")

        if location not in locations:
            flash("Please choose a valid location.", "error")
            return redirect(url_for("optimize"))

        try:
            budget = Decimal(budget_raw)
            if not budget.is_finite() or budget < 0:
                raise ValueError
            budget = budget.quantize(Decimal("0.01"))
        except (InvalidOperation, ValueError):
            flash("Enter a valid budget.", "error")
            return redirect(url_for("optimize"))

        products = get_location_products(location)
        stores = get_location_stores(location)
        product_ids = {row["product"].id for row in products}

        raw_quantities = {
            product_id: (request.form.get(f"qty_{product_id}", "0").strip() or "0")
            for product_id in product_ids
        }
        quantities = {}

        context = {
            "step": "basket",
            "form": form,
            "location": location,
            "budget": budget,
            "products": products,
            "stores": stores,
            "categories": get_product_categories(products),
            "quantities": raw_quantities,
            "plan": None,
        }

        for product_id, raw in raw_quantities.items():
            try:
                quantity = int(raw)
            except ValueError:
                flash("Quantities must be whole numbers.", "error")
                return render_template("optimize.html", **context)

            if quantity < 0:
                flash("Quantities cannot be negative.", "error")
                return render_template("optimize.html", **context)

            if quantity > 9999:
                flash("Quantities must be 9999 or less.", "error")
                return render_template("optimize.html", **context)

            if quantity > 0:
                quantities[product_id] = quantity

        if not quantities:
            flash("Enter a quantity for at least one food.", "error")
            return render_template("optimize.html", **context)

        context["quantities"] = quantities
        context["plan"] = calculate_plan(location, budget, quantities)
        return render_template("optimize.html", **context)

    if form.validate_on_submit():
        location = form.location.data

        try:
            budget = form.budget.data.quantize(Decimal("0.01"))
        except (InvalidOperation, AttributeError):
            flash("Enter a valid budget.", "error")
            return redirect(url_for("optimize"))

        products = get_location_products(location)

        return render_template(
            "optimize.html",
            step="basket",
            form=form,
            location=location,
            budget=budget,
            products=products,
            stores=get_location_stores(location),
            categories=get_product_categories(products),
            quantities={},
            plan=None,
        )

    return render_template(
        "optimize.html",
        step="setup",
        form=form,
        locations=locations,
    )


@app.route("/contributions")
def contributions():
    manila = timezone(timedelta(hours=8))

    rows = db.session.execute(
            db.select(PriceHistory, Product, Store)
            .join(ProductStore, PriceHistory.product_store_id == ProductStore.id)
            .join(Product, ProductStore.product_id == Product.id)
            .join(Store, ProductStore.store_id == Store.id)
            .where(PriceHistory.user_id == current_user.id)
            .order_by(PriceHistory.recorded_at.desc())
        ).all()

    entries = []
    
    for history, product, store in rows:
        recorded = history.recorded_at
    
        if recorded.tzinfo is None:
            recorded = recorded.replace(tzinfo=timezone.utc)
    
        entries.append({
            "date": recorded.astimezone(manila).strftime("%b %d, %Y %I:%M %p"),
            "food": product.name,
            "category": product.category,
            "store": store.name,
            "location": store.location,
            "price": history.price
        })

    stats = {
        "prices": len(entries),
        "foods": len({e["food"] for e in entries}),
        "stores": len({(e["store"], e["location"]) for e in entries}),
        "locations": len({e["location"] for e in entries}),
    }

    return render_template("contributions.html", entries=entries, stats=stats)

#dagdagan ng image pag di tinamad, may default image based on category(?)
@app.route("/browse")
def browse():
    latest_prices = (db.select(PriceHistory.product_store_id, db.func.max(PriceHistory.id).label("latest_id"))
        .group_by(PriceHistory.product_store_id).subquery())
    store_counts = (
        db.select(ProductStore.product_id, db.func.count(db.distinct(ProductStore.store_id)).label("store_count"))
        .group_by(ProductStore.product_id).subquery())
    product_prices = (
        db.select(ProductStore.product_id, PriceHistory.price, PriceHistory.recorded_at,
            db.func.row_number().over(partition_by=ProductStore.product_id, order_by=PriceHistory.recorded_at.desc()).label("rank"))
        .join(PriceHistory, PriceHistory.product_store_id == ProductStore.id)
        .join(latest_prices, latest_prices.c.latest_id == PriceHistory.id)
        .subquery()
    )

    category = request.args.get("category", "")

    query = (
        db.select(Product, product_prices.c.price, store_counts.c.store_count)
        .join(product_prices, product_prices.c.product_id == Product.id)
        .join(store_counts, store_counts.c.product_id == Product.id)
        .where(product_prices.c.rank == 1)
    )

    if category in CATEGORIES:
        query = query.where(Product.category == category)

    rows = db.session.execute(query.order_by(Product.name)).all()

    products = []

    for product, price, store_count in rows:
        products.append({
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "description": product.description,
            "price": price,
            "stores": store_count
        })
    
    return render_template("browse.html", products=products, categories=CATEGORIES, category=category)

@app.route("/product/<int:product_id>")
def product(product_id):
    product = db.session.get(Product, product_id)
    if product is None:
        return "Product not found", 404
    rows = db.session.execute(db.select(Product, ProductStore, Store, PriceHistory)
        .join(ProductStore, ProductStore.product_id == Product.id)
        .join(Store, Store.id == ProductStore.store_id)
        .outerjoin(PriceHistory, PriceHistory.product_store_id == ProductStore.id)
        .where(Product.id == product_id).order_by(Store.name, PriceHistory.recorded_at.desc())
    ).all()

    stores = {}
    for product, listing, store, history in rows:
        if store.id not in stores:
            stores[store.id] = {
                "name": store.name,
                "location": store.location,
                "prices": []
            }

        if history:
            stores[store.id]["prices"].append({
                "price": history.price,
                "recorded_at": history.recorded_at
            })

    return render_template("product.html", product=product, stores=stores)

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

@app.route('/nukedb')
def nuke_db():
    
    db.drop_all()
    db.create_all()
    
    return redirect('/')

@app.route('/update')
def deploy():
    pa_token = os.environ.get("PA_API_TOKEN")
    
    result = subprocess.run(
        ['git', 'pull'], 
        cwd='/home/CommunityFoodPrice/foodprice',
        capture_output=True, 
        text=True
    )
    
    if result.returncode != 0:
        return f"there was an error running `git pull`. Error: {result.stderr}"
        
    reload_url = f"https://www.pythonanywhere.com/api/v0/user/CommunityFoodPrice/webapps/CommunityFoodPrice.pythonanywhere.com/reload/"
    req = urllib.request.Request(reload_url, method='POST')
    req.add_header('Authorization', f'Token {pa_token}')

    try:
        urllib.request.urlopen(req)
    except Exception as error:
        return f"git pulled successfully but api failed. error: {error}"

    return redirect('/')