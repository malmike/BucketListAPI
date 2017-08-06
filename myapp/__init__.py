"""
This is the script for initialising the flask application
"""
from flask import Flask

from myapp.api.auth_endpoints import auth_blueprint
from myapp.api.bucketlist_endpoints import bucketlist_blueprint
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
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')
    app.register_blueprint(bucketlist_blueprint, url_prefix='/api/v1')
    return app

