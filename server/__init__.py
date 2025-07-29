from flask import Flask
from flask_cors import CORS
import os

from server.controllers.page_routes import page_bp
from server.controllers.transcript_controller import transcript_bp
from server.exceptions.api_exceptions import register_error_handlers

def create_app():
    # Get the directory of the current file
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    app = Flask(__name__, 
                static_folder=os.path.join(basedir, 'static'),
                static_url_path='/static',
                template_folder=os.path.join(basedir, 'templates'))
    
    # Configure CORS for deployment
    CORS(app, origins=["*"])

    # Register route page
    app.register_blueprint(page_bp)

    # Register route api
    app.register_blueprint(transcript_bp)

    # Register global error handlers
    register_error_handlers(app)

    return app
