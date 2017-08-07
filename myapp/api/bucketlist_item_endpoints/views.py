"""
This file contains the endpoints for bucketlists items
"""
from flask_restplus import Namespace, Resource, abort, fields
from flask import request, g
from myapp.models.bucketlist import BucketList
from myapp.models.bucketlist_item import BucketListItem
from myapp.utilities.Utilities import auth

bucketlist_item_api = Namespace('bucketlist', description='Bucketlist And Bucketlist Items')

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
    @bucketlist_item_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @bucketlist_item_api.response(200, 'Successful Retreival of bucketlist items')
    @bucketlist_item_api.response(400, 'No existing bucketlist with the id passes')
    @bucketlist_item_api.marshal_with(BUCKETLISTITEM, as_list=True)
    def get(self, bucketlist_id):
        """
        Handles the retreival of a bucketlist's items
        """
        bucketlist = BucketList.query.filter_by(user_id=g.current_user.id, id=bucketlist_id).first()
        if bucketlist:
            return bucketlist.bucketlist_items
        abort(400, 'Bucketlist with ID {} not found in the database'.format(bucketlist_id))

    


