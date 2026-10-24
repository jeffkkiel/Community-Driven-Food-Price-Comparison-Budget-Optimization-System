from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import *


@app.route("/")
def dashboard():
    comprForm = CompareForm()
    return render_template("dashboard.html")


@app.route("/#popup-add", methods=["POST"])
def add_price():
    form = ProductForm()
    if form.validate_on_submit():
        flash('Adding Product "{}"'.format(form.product))
        return redirect(url_for('/'))
