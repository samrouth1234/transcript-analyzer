from flask import Blueprint, render_template, send_from_directory, current_app
import os

page_bp = Blueprint("pages", __name__)

@page_bp.route("/")
def home_page():
    return render_template("index.html")

@page_bp.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files for deployment"""
    try:
        static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
        current_app.logger.info(f"Serving static file: {filename} from {static_dir}")
        return send_from_directory(static_dir, filename)
    except Exception as e:
        current_app.logger.error(f"Error serving static file {filename}: {e}")
        return f"Static file not found: {filename}", 404
