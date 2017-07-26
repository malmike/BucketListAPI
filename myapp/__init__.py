"""
This is the script for initialising the flask application
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app(config_module):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_module)
    return app