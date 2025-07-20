from flask import Blueprint, render_template

page_bp = Blueprint("pages", __name__)

@page_bp.route("/")
def home_page():
    return render_template("index.html")
