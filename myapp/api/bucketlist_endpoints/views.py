"""
This file contains the endpoints for bucketlists
"""
from flask_restplus import Namespace, Resource, abort, fields
from flask import request, g
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
    @bucketlist_api.header('x-access-token', 'Access Token', required=True)
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

        bucketlist = BucketList(name=name, user_id=g.current_user.id)

        try:
            check = bucketlist.save_bucketlist()
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


    @bucketlist_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @bucketlist_api.response(200, 'Successful Retreival of bucketlists')
    @bucketlist_api.response(400, 'User has no single bucketlist')
    @bucketlist_api.marshal_with(BUCKETLIST, as_list=True)
    def get(self):
        """
        Retrieves existing bucketlists for specific user
        """
        if g.current_user.bucketlists:
            return g.current_user.bucketlists, 200
        return abort(400, 'User has no single bucketlist')


@bucketlist_api.route('/<int:bucketlist_id>', endpoint='individual_bucketlist')
class IndividualBucketList(Resource):
    """
    Class contains methods specific to an individual bucketlist
    """
    @bucketlist_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @bucketlist_api.response(200, 'Successfully Retrieved Bucketlist')
    @bucketlist_api.response(400, 'No existing bucketlist with the id passes')
    @bucketlist_api.marshal_with(BUCKETLIST)
    def get(self, bucketlist_id):
        """
        Retrieves existing bucketlists for specific user
        """
        bucketlists = g.current_user.bucketlists
        _bucketlist = next(
            (bucketlist for bucketlist in bucketlists if bucketlist.id == bucketlist_id),
            None
        )
        if _bucketlist:
            return _bucketlist
        return abort(400, 'Bucketlist with ID {} not found in the database'.format(bucketlist_id))


    @bucketlist_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @bucketlist_api.response(200, 'Successfully Updated Bucketlist')
    @bucketlist_api.response(400, 'No existing bucketlist with the id passes')
    @bucketlist_api.marshal_with(BUCKETLIST)
    def put(self, bucketlist_id):
        """
        Updates existing bucketlists for specific user
        """
        put_data = request.get_json()
        name = put_data.get('name')
        bucketlist = BucketList.query.filter_by(user_id=g.current_user.id, id=bucketlist_id).first()
        if bucketlist:
            bucketlist.name = name
            bucketlist.save_bucketlist()
            return bucketlist, 200
        return abort(400, 'Bucketlist with ID {} not found in the database'.format(bucketlist_id))


    @bucketlist_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @bucketlist_api.response(200, 'Successfully Deleted Bucketlist')
    @bucketlist_api.response(400, 'No existing bucketlist with the id passes')
    def delete(self, bucketlist_id):
        """
        Retrieves existing bucketlists for specific user
        """
        bucketlist = BucketList.query.filter_by(user_id=g.current_user.id, id=bucketlist_id).first()
        if bucketlist:
            bucketlist.delete_bucketlist()
            response = {
                'status': 'success',
                'message': 'Bucketlist with ID {} deleted'.format(bucketlist_id)
            }
            return response, 200
        return abort(400, 'Bucketlist with ID {} not found in the database'.format(bucketlist_id))
