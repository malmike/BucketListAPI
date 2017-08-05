"""
Initializes the auth endpoint module with blueprints
"""
from flask import Blueprint
from flask_restplus import Api
from .views import auth_api

auth_blueprint = Blueprint('auth', __name__)
api_v1 = Api(auth_blueprint)

# Set up paths for the auth endpoints
##User registration path
api_v1.add_namespace(auth_api)
