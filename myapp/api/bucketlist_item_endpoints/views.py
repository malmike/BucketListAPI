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
        'id':fields.Integer(),
        'name': fields.String(
            required=True,
            description="Bucketlist Item Name",
            example="test_bucketlist_item"),
        'date_created': fields.DateTime(required=False, attribute='created'),
        'date_modified': fields.DateTime(required=False, attribute='modified'),
        'bucketlist_id': fields.Integer(required=True),
        'completed': fields.Boolean(),
        'finished_by': fields.Date(required=True),
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
        return abort(400, 'Bucketlist with ID {} not found in the database'.format(bucketlist_id))


    @bucketlist_item_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @bucketlist_item_api.response(200, 'Successful Added Bucketlist item')
    @bucketlist_item_api.response(400, 'No existing bucketlist with the id passes')
    @bucketlist_item_api.response(500, 'Internal Server Error')
    @bucketlist_item_api.doc(model='BucketlistItem', body=BUCKETLISTITEM)
    def post(self, bucketlist_id):
        """
        Handles the adding bucketlist items
        """
        post_data = request.get_json()
        name = post_data.get('name')
        finished_by = post_data.get('finished_by')
        bucketlist = BucketList.query.filter_by(user_id=g.current_user.id, id=bucketlist_id).first()
        try:
            if bucketlist:
                bucketlist_item = BucketListItem(
                    name=name,
                    finished_by=finished_by,
                    bucketlist_id = bucketlist.id
                )
                bucketlist_item.save_bucketlist_item()
                response = {
                    'status': 'success',
                    'message': 'Bucket list item added'
                }
                return response, 201
            abort(400, 'Bucketlist with ID {} not found in the database'.format(bucketlist_id))
        except Exception as e:
            return abort(500, message='Error adding bucketlist item:{}'.format(e.message))


@bucketlist_item_api.route(
    '/<int:bucketlist_id>/items/<item_id>',
    endpoint='single_bucketlist_item'
)
class SingleBucketListItem(Resource):
    """
    Class handles request made towards a single bucketlist item
    """
    @bucketlist_item_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @bucketlist_item_api.response(200, 'Successfully Updated Bucketlist')
    @bucketlist_item_api.response(400, 'No existing bucketlist or bucketlist_item with the ids passed')
    @bucketlist_item_api.marshal_with(BUCKETLISTITEM)
    def put(self, bucketlist_id, item_id):
        """
        Handles put requests to alter a single bucketlist item
        """
        put_data = request.get_json()
        name = put_data.get('name') or None
        completed = put_data.get('completed') or None

        bucketlist = BucketList.query.filter_by(user_id=g.current_user.id, id=bucketlist_id).first()
        if bucketlist:
            item = BucketListItem.query.filter_by(
                bucketlist_id=bucketlist_id,
                id=item_id
            ).first()
            if item:
                try:
                    item.name = name if name is not None else item.name
                    item.completed = completed if completed is not None else item.completed
                    item.save_bucketlist_item()
                    return item, 200
                except Exception as e:
                    return abort(500, message='Error updating bucketlist item:{}'.format(e.message))
            return abort(400, 'Bucketlist Item with ID {} not found in the database'.format(item_id))

        return abort(400, 'Bucketlist with ID {} not found in the database'.format(item_id))


    @bucketlist_item_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @bucketlist_item_api.response(200, 'Successfully Updated Bucketlist')
    @bucketlist_item_api.response(400, 'No existing bucketlist or bucketlist_item with the ids passed')
    def delete(self, bucketlist_id, item_id):
        """
        Handles delete requests to for bucketlist item
        """
        bucketlist = BucketList.query.filter_by(user_id=g.current_user.id, id=bucketlist_id).first()
        if bucketlist:
            item = BucketListItem.query.filter_by(
                bucketlist_id=bucketlist_id,
                id=item_id
            ).first()
            if item:
                try:
                    item.delete_bucketlist_item()
                    response = {
                        'status': 'success',
                        'message': 'Bucketlist Item with ID {} deleted'.format(item_id)
                    }
                    return response, 200
                except Exception as e:
                    return abort(500, message='Error updating bucketlist item:{}'.format(e.message))
            return abort(
                400,
                'Bucketlist Item with ID {} not found in the database'.format(item_id)
            )

        return abort(
            400,
            'Bucketlist with ID {} not found in the database'.format(item_id)
        )