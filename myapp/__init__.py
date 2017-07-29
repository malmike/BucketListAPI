"""
This is the script for initialising the flask application
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
app = Flask(__name__, instance_relative_config=True)
bcrypt = Bcrypt(app)

def create_app(config_module):
    """
    This creates an instance of the flask application basing on
    the configurations passed to it
    """
    app.config.from_object(config_module)
    db.init_app(app)
