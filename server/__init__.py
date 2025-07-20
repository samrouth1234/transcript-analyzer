from flask import Flask
from flask_cors import CORS

from server.controllers.page_routes import page_bp
from server.controllers.transcript_controller import transcript_bp
from server.exceptions.api_exceptions import register_error_handlers
from server.utils.config import Config


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(Config)

    # Register route page
    app.register_blueprint(page_bp)

    # Register route api
    app.register_blueprint(transcript_bp)

    # Register global error handlers
    register_error_handlers(app)

    return app
