from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import *


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
def add_price():
    return render_template("add_price.html", form=ProductForm())


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
