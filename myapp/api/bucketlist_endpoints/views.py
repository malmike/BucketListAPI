"""
This file contains the endpoints for bucketlists
"""
from flask_restplus import Namespace, Resource, abort, fields, marshal
from flask import request, g, url_for
from flask_sqlalchemy import Pagination
from sqlalchemy import desc

from myapp.models.bucketlist import BucketList
from myapp.utilities.Utilities import auth, strip_white_space
from myapp.api.bucketlist_item_endpoints.views import BUCKETLISTITEM
from instance.config import Config

bucketlist_api = Namespace('bucketlist', description='Bucketlist Details')

BUCKETLIST = bucketlist_api.model(
    'Bucketlist',
    {
        'id':fields.Integer(),
        'name': fields.String(
            required=True,
            description="Bucketlist Name",
            example="test bucketlist"),
        'date_created': fields.DateTime(required=False, attribute='created'),
        'date_modified': fields.DateTime(required=False, attribute='modified'),
        'created_by':fields.Integer(required=True, attribute='user_id'),
        'bucketlist_items': fields.Nested(BUCKETLISTITEM)
    }
)

bucketlist_parser = bucketlist_api.parser()
bucketlist_parser.add_argument('q', type=str, help='Search term for querying bucketlist', required=False)
bucketlist_parser.add_argument('limit', type=str, help='Sets the limit for pargination', required=False)
bucketlist_parser.add_argument('page', type=str)

bucketlist_name_parser = bucketlist_api.parser()
bucketlist_name_parser.add_argument('name', type=str, help='Bucketlist name', required=True)

BUCKETLIST_NAME = bucketlist_api.model(
    'bucketlist_name',
    {
        'name': fields.String(
            required=True,
            description="Bucketlist Name",
            example="rename bucketlist")
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
    @bucketlist_api.response(400, 'Bad Request')
    @bucketlist_api.response(500, 'Internal Server Error')
    @bucketlist_api.doc(model='Bucketlist', body=BUCKETLIST)
    def post(self):
        """
        Handles adding of new bucketlists
        """
        post_data = request.get_json()
        name = strip_white_space(post_data.get('name'))

        if not name:
            return abort(400, "Bucket list name must be provided")

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
                return response, 400
        except Exception as e:
            return abort(500, message='Error creating your account:{}'.format(e.message))


    @bucketlist_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @bucketlist_api.response(200, 'Successful Retreival of bucketlists')
    @bucketlist_api.response(400, 'Bad Request')
    @bucketlist_api.response(404, 'Pages cannot be negative')
    @bucketlist_api.expect(bucketlist_parser)
    def get(self):
        """
        Retrieves existing bucketlists for specific user
        """
        search_term = request.args.get('q') or None
        limit = request.args.get('limit') or Config.DEFAULT_PAGINATION_NUMBER
        page_limit = 100 if int(limit) > 100 else int(limit)
        page = request.args.get('page') or 1

        if page_limit < 1 or page < 1:
            return abort(404, 'Page or Limit cannot be negative values')

        bucketlist_data = BucketList.query.filter_by(user_id=g.current_user.id).\
            order_by(desc(BucketList.created))
        if bucketlist_data.all():
            bucketlists = bucketlist_data

            if search_term:
                bucketlists = bucketlist_data.filter(
                    BucketList.name.ilike('%'+search_term+'%')
                )

            bucketlist_paged = bucketlists.paginate(
                page=page, per_page=page_limit, error_out=True
            )
            result = dict(data=marshal(bucketlist_paged.items, BUCKETLIST))

            pages = {
                'page': page, 'per_page': page_limit,
                'total_data': bucketlist_paged.total, 'pages': bucketlist_paged.pages
            }

            if page == 1:
                pages['prev_page'] = url_for('api.bucketlist')+'?limit={}'.format(page_limit)

            if page > 1:
                pages['prev_page'] = url_for('api.bucketlist')+'?limit={}&page={}'.format(page_limit, page-1)

            if page < bucketlist_paged.pages:
                pages['next_page'] = url_for('api.bucketlist')+'?limit={}&page={}'.format(page_limit, page+1)

            result.update(pages)
            return result

        return abort(400, 'User has no single bucketlist')


@bucketlist_api.route('/<int:bucketlist_id>', endpoint='individual_bucketlist')
class IndividualBucketList(Resource):
    """
    Class contains methods specific to an individual bucketlist
    """
    @bucketlist_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @bucketlist_api.response(200, 'Successfully Retrieved Bucketlist')
    @bucketlist_api.response(400, 'Bad Request')
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
    @bucketlist_api.response(400, 'Bad Request')
    @bucketlist_api.doc(model='bucketlist_name', body=BUCKETLIST_NAME)
    @bucketlist_api.marshal_with(BUCKETLIST)
    def put(self, bucketlist_id):
        """
        Updates existing bucketlists for specific user
        """
        print(request)
        put_data = request.get_json()
        name = strip_white_space(put_data.get('name'))
        if not name:
            return abort(400, "Bucket list name must be provided")
        bucketlist = BucketList.query.filter_by(user_id=g.current_user.id, id=bucketlist_id).first()
        if bucketlist:
            if bucketlist.save_bucketlist(name):
                return bucketlist, 200
            return abort(409, "Bucketlist exists")
        return abort(400, 'Bucketlist with ID {} not found in the database'.format(bucketlist_id))


    @bucketlist_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @bucketlist_api.response(200, 'Successfully Deleted Bucketlist')
    @bucketlist_api.response(400, 'Bad Request')
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
