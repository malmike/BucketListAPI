from flask import Blueprint
from flask_restplus import Api
from .auth_endpoints.views import auth_api
from .bucketlist_endpoints.views import bucketlist_api

api_v1_blueprint = Blueprint('api', __name__)

api_v1 = Api(api_v1_blueprint)

api_v1.add_namespace(auth_api)
api_v1.add_namespace(bucketlist_api)