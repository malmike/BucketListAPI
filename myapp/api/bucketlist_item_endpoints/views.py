"""
This file contains the endpoints for bucketlists items
"""
from flask_restplus import Namespace, Resource, abort, fields
from flask import request, g
from myapp.models.bucketlist import BucketList
from myapp.models.bucketlist_item import BucketListItem
from myapp.utilities.Utilities import auth, strip_white_space

bucketlist_item_api = Namespace('bucketlist', description='Bucketlist And Bucketlist Items')

BUCKETLISTITEM = bucketlist_item_api.model(
    'BucketlistItem',
    {
        'id':fields.Integer(),
        'name': fields.String(
            required=True,
            description="Bucketlist Item Name",
            example="test bucketlist item"),
        'date_created': fields.DateTime(required=False, attribute='created'),
        'date_modified': fields.DateTime(required=False, attribute='modified'),
        'bucketlist_id': fields.Integer(required=True),
        'completed': fields.Boolean(default=False),
        'finished_by': fields.Date(required=True),
    }
)

ADD_BUCKETLISTITEM = bucketlist_item_api.model(
    'addBucketlistItem',
    {
        'name': fields.String(
            required=True,
            description="Bucketlist Item Name",
            example="test bucketlist item"),
        'finished_by': fields.Date(required=True)
    }
)

UPDATE_ITEM = bucketlist_item_api.model(
    'update_item',{
        'name': fields.String(description='Bucketlist Item name', example='new item name', required=False),
        'completed': fields.String(
            default="false", description="Takes string values `true` or `false`", required=True
        )
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
    @bucketlist_item_api.response(404, 'No existing bucketlist with the id passes')
    @bucketlist_item_api.marshal_with(BUCKETLISTITEM, as_list=True)
    def get(self, bucketlist_id):
        """
        Handles the retreival of a bucketlist's items
        """
        bucketlist = BucketList.query.filter_by(user_id=g.current_user.id, id=bucketlist_id).first()
        if bucketlist:
            return bucketlist.bucketlist_items, 200
        return abort(404, 'Bucketlist with ID {} not found in the database'.format(bucketlist_id))


    @bucketlist_item_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @bucketlist_item_api.response(201, 'Successful Added Bucketlist item')
    @bucketlist_item_api.response(400, 'Bad Request')
    @bucketlist_item_api.response(404, 'Not Found')
    @bucketlist_item_api.response(409, 'Bucketlist Item Exists')
    @bucketlist_item_api.doc(model='addBucketlistItem', body=ADD_BUCKETLISTITEM)
    def post(self, bucketlist_id):
        """
        Handles the adding bucketlist items
        """
        post_data = request.get_json()
        name = strip_white_space(post_data.get('name'))
        finished_by = strip_white_space(post_data.get('finished_by'), skip_check_symbols=True)
        if not name or not finished_by:
            return abort(400, "Bucketlist item name and finished_by should be provided")

        bucketlist = BucketList.query.filter_by(user_id=g.current_user.id, id=bucketlist_id).first()
        if bucketlist:
            bucketlist_item = BucketListItem(
                name=name,
                finished_by=finished_by,
                bucketlist_id = bucketlist.id
            )
            if bucketlist_item.save_bucketlist_item():
                response = {
                    'status': 'success',
                    'message': 'Bucket list item added'
                }
                return response, 201
            return abort(409, 'Bucketlist Item Exists')
        return abort(404, 'Bucketlist with ID {} not found in the database'.format(bucketlist_id))
    


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
    @bucketlist_item_api.response(201, 'Successfully Updated Bucketlist')
    @bucketlist_item_api.response(400, 'Bad Request')
    @bucketlist_item_api.response(404, 'Not Found')
    @bucketlist_item_api.response(409, 'Bucket List Item Already Exists')
    @bucketlist_item_api.marshal_with(BUCKETLISTITEM)
    @bucketlist_item_api.doc(model='update_item', body=UPDATE_ITEM)
    def put(self, bucketlist_id, item_id):
        """
        Handles put requests to alter a single bucketlist item
        """
        put_data = request.get_json()
        name = strip_white_space(put_data.get('name') or '') or None
        completed = str(put_data.get('completed')) or None
        if completed is not None and isinstance(completed, str):
            completed = completed.strip()
            completed = completed.capitalize()
        test_completed = completed is None or not completed.isalnum()
        verify_completed = completed == 'True' or completed == 'False'
        if completed is not None and not verify_completed:
            return abort(400, 'Completed must either be true or false')

        if not name and test_completed:
            return abort(400, 'No data sent for updating or inaccurate data provided')

        bucketlist = BucketList.query.filter_by(user_id=g.current_user.id, id=bucketlist_id).first()
        if bucketlist:
            item = BucketListItem.query.filter_by(
                bucketlist_id=bucketlist_id,
                id=item_id
            ).first()
            if item:
                if item.save_bucketlist_item(
                    name = name, 
                    completed = completed
                ):
                    return item, 201
                return abort(409, "Bucket list item already exists")
            return abort(404, 'Bucketlist Item with ID {} not found in the database'.format(item_id))

        return abort(404, 'Bucketlist with ID {} not found in the database'.format(item_id))


    @bucketlist_item_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @bucketlist_item_api.response(200, 'Successfully Deleted Bucketlist')
    @bucketlist_item_api.response(404, 'Not Found')
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
                404,
                'Bucketlist Item with ID {} not found in the database'.format(item_id)
            )

        return abort(
            404,
            'Bucketlist with ID {} not found in the database'.format(item_id)
        )