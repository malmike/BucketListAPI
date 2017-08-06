"""
Initializes the bucketlist endpoint module with blueprints
"""
from flask import Blueprint
from flask_restplus import Api
from .views import bucketlist_api

bucketlist_blueprint = Blueprint('bucketlist', __name__)
api_v1 = Api(bucketlist_blueprint)

# Set up paths for the auth endpoints
##User registration path
api_v1.add_namespace(bucketlist_api)