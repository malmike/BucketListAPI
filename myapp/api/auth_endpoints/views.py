"""
This file contains the endpoints for authentication
i.e user registration, user authentication, user verification
and logout
"""
from flask_restplus import Namespace, Resource, abort, fields
from flask import request
from re import search
from myapp.models.user import User

auth_api = Namespace('auth', description='User authentication and registration')

USER = auth_api.model(
    'User',
    {
        'email':fields.String(required=True, description="User's Email", example="test@test.com"),
        'password':fields.String(
            required=True,
            description="User's Password",
            example="test_password"
        )
    }
)

@auth_api.route('/register', endpoint='registration')
class RegisterUser(Resource):
    """
    Handles requests for registering a new user
    """
    @auth_api.response(201, 'Successful User Registration')
    @auth_api.response(409, 'User Data is invalid or User Exists')
    @auth_api.response(
        500,
        'Server encountered an unexpected condition that prevented it from fulfilling the request.'
    )
    @auth_api.doc(model='User', body=USER)
    def post(self):
        """
        Handles post requests for registration of a new user
        """
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')

        if not User.validate_email(email):
            return abort(409, 'Invalid Email Address')

        user = User(email=email, password=password)

        try:
            check = user.add_user()
            if check:
                auth_token = user.generate_authentication_token()
                response = {
                    'status': 'success',
                    'message': 'Successfully Registered',
                    'auth_token': auth_token
                }
                return response, 201
            else:
                response = {'status': 'fail', 'message': 'User Exists'}
                return response, 409
        except Exception as e:
            return abort(500, message='Error creating your account:{}'.format(e.message))


@auth_api.route('/login', endpoint='login')
class AuthenticateUser(Resource):
    """
    Handles requests for authentication of a user, based on the user's email
    and password
    """
    def post(self):
        """
        Handles post requests for authentication of a user
        """
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')

        if not User.validate_email(email):
            return abort(409, 'Invalid Email Address')

        user = User.query.filter_by(email=email).first()

        if user and user.verify_password(password):
            auth_token = user.generate_authentication_token()
            response = {
                'status': 'success',
                'message': 'Login Successful',
                'auth_token': auth_token
            }
            return response, 201
        response = {
            'status': 'fail',
            'message': 'Failed to authenticate user'
        }
        return response, 401





