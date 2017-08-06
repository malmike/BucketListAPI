"""
This file contains the endpoints for authentication
i.e user registration, user authentication, user verification
and logout
"""
from flask_restplus import Namespace, Resource, abort, fields
from flask import request, g
from re import search
from myapp.models.bucketlist import BucketList
from myapp.utilities.Utilities import auth

bucketlist_api = Namespace('bucketlist', description='Bucketlist Details')

BUCKETLIST = bucketlist_api.model(
    'bucketlist',
    {
        'name': fields.String(
            required=True,
            description="Bucketlist Name",
            example="test_bucketlist"),
        'date_created': fields.DateTime(attribute='created'),
        'date_modified': fields.DateTime(attribute='modified'),
        'created_by':fields.Integer(attribute='user_id')
    }
)


@auth.login_required
@bucketlist_api.route('/bucketlist', endpoint='bucketlist')
class BucketListEndPoint(Resource):
    """
    Class contains operations which handle requests specific to a bucketlist
    """
    pass
