from flask import Blueprint, render_template

page_bp = Blueprint("pages", __name__)

@page_bp.route("/")
def home_page():
    return render_template("index.html")

# @page_bp.route("/about")
# def about_page():
#     return render_template("about.html")
#
# @page_bp.route("/audio")
# def audio_page():
#     return render_template("audio.html")
#
# @page_bp.route("/transcript")
# def transcript_page():
#     return render_template("transcript.html")
