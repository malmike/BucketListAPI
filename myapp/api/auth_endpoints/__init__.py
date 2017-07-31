"""
Initializes the auth endpoint module with blueprints
"""
from flask import Blueprint
from flask_restplus import Api
from myapp.api.auth_endpoints.views import RegisterUser

auth_blueprint = Blueprint('auth', __name__)
api_v1 = Api(auth_blueprint)

# Set up paths for the auth endpoints
##User registration path
api_v1.add_resource(RegisterUser, '/auth/register', endpoint='register_endpoint')
