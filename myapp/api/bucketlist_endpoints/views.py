"""
This file contains the endpoints for bucketlists
"""
from flask_restplus import Namespace, Resource, abort, fields
from flask import request, g
from re import search
from myapp.models.bucketlist import BucketList
from myapp.utilities.Utilities import auth

bucketlist_api = Namespace('bucketlist', description='Bucketlist Details')

BUCKETLIST = bucketlist_api.model(
    'Bucketlist',
    {
        'name': fields.String(
            required=True,
            description="Bucketlist Name",
            example="test_bucketlist"),
        'date_created': fields.DateTime(required=False, attribute='created'),
        'date_modified': fields.DateTime(required=False, attribute='modified'),
        'created_by':fields.Integer(required=True, attribute='user_id')
    }
)


@bucketlist_api.route('', endpoint='bucketlist')
class BucketListEndPoint(Resource):
    """
    Class contains operations which handle requests specific to a bucketlist
    """
    @auth.login_required
    @bucketlist_api.response(201, 'Successful Bucketlist Added')
    @bucketlist_api.response(409, 'Bucketlist Exists')
    @bucketlist_api.response(
        500,
        'Server encountered an unexpected condition that prevented it from fulfilling the request.'
    )
    @bucketlist_api.doc(model='Bucketlist', body=BUCKETLIST)
    def post(self):
        """
        Handles adding of new bucketlists
        """
        post_data = request.get_json()
        name = post_data.get('name')
        created_by = post_data.get('created_by')

        bucketlist = BucketList(name=name, user_id=created_by)

        try:
            check = bucketlist.add_bucketlist()
            if check:
                response = {
                    'status': 'success',
                    'message': 'Bucketlist Added'
                }
                return response, 201
            else:
                response = {'status': 'fail', 'message': 'Bucketlist Exists'}
                return response, 409
        except Exception as e:
            return abort(500, message='Error creating your account:{}'.format(e.message))

