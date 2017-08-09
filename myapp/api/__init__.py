from flask import Blueprint
from flask_restplus import Api
from flask_cors import CORS
from .auth_endpoints.views import auth_api
from .bucketlist_endpoints.views import bucketlist_api
from .bucketlist_item_endpoints.views import bucketlist_item_api

api_v1_blueprint = Blueprint('api', __name__)
CORS(api_v1_blueprint)

api_v1 = Api(api_v1_blueprint)

api_v1.add_namespace(auth_api)
api_v1.add_namespace(bucketlist_api)
api_v1.add_namespace(bucketlist_item_api)
