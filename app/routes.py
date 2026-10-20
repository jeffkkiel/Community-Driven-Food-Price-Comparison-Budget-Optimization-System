from flask import render_template
from app import app


@app.route("/")
def dashboard():
    return render_template("dashboard.html")
