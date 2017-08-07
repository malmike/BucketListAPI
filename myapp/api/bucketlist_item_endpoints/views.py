"""
This file contains the endpoints for bucketlists items
"""
from flask_restplus import Namespace, Resource, abort, fields
from flask import request, g
from myapp.models.bucketlist_item import BucketListItem
from myapp.utilities.Utilities import auth

bucketlist_item_api = Namespace('bucketlist_item', description='Bucketlist Items Details')

BUCKETLISTITEM = bucketlist_item_api.model(
    'BucketlistItem',
    {
        'name': fields.String(
            required=True,
            description="Bucketlist Item Name",
            example="test_bucketlist_item"),
        'date_created': fields.DateTime(required=False, attribute='created'),
        'date_modified': fields.DateTime(required=False, attribute='modified'),
        'bucketlist_id': fields.Integer(required=True),
        'completed': fields.Boolean(),
        'finished_by': fields.DateTime(required=True),
    }
)

@bucketlist_item_api.route('/<int:bucketlist_id>/items/', endpoint='bucketlist_item')
class BucketListItemEndPoint(Resource):
    """
    Class contains operations which handle requests specific to a bucketlist items
    """
