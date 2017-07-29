"""
This is the script for initialising the flask application
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_module):
    """
    This creates an instance of the flask application basing on
    the configurations passed to it
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_module)
    db.init_app(app)
    return app