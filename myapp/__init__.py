"""
This is the script for initialising the flask application
"""
from flask import Flask

from myapp.api import api_v1_blueprint
from .models.base_model import db

def create_app(config_module):
    """
    This creates an instance of the flask application basing on
    the configurations passed to it
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_module)
    db.init_app(app)

    # Register the blue prints
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')
    return app
