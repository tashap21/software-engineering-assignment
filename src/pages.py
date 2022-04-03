from flask import Blueprint, render_template

pages = Blueprint("pages", __name__)


@pages.route("/")
@pages.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
