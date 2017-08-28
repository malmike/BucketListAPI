"""
This file contains the endpoints for authentication
i.e user registration, user authentication, user verification
and logout
"""
from re import search

from flask_restplus import Namespace, Resource, abort, fields, marshal
from flask import request, g

from myapp.models.user import User
from myapp.models.blacklist_token import BlackListToken
from myapp.utilities.Utilities import validate_email, strip_white_space, auth

auth_api = Namespace('auth', description='User authentication and registration')

USER = auth_api.model(
    'User',
    {
        'fname':fields.String(required=True, description="User's First Name", example="Fname"),
        'lname':fields.String(required=True, description="User's Last Name", example="Lname"),
        'email':fields.String(required=True, description="User's Email", example="test@test.com"),
        'password':fields.String(
            required=True,
            description="User's Password",
            example="testpassword"
        )
    }
)

LOGIN = auth_api.model(
    'login',
    {
        'email':fields.String(required=True, description="User's Email", example="test@test.com"),
        'password':fields.String(
            required=True,
            description="User's Password",
            example="testpassword"
        )
    }
)

@auth_api.route('/register', endpoint='registration')
class RegisterUser(Resource):
    """
    Handles requests for registering a new user
    """
    @auth_api.response(201, 'Successful User Registration')
    @auth_api.response(400, 'Bad Request')
    @auth_api.response(500,'Internal Server Error')
    @auth_api.doc(model='User', body=USER)
    def post(self):
        """
        Handles post requests for registration of a new user
        """
        post_data = request.get_json()
        fname = strip_white_space(post_data.get('fname')) or None
        lname = strip_white_space(post_data.get('lname')) or None
        email = strip_white_space(post_data.get('email'), skip_check_symbols=True) or None
        password = strip_white_space(post_data.get('password')) or None

        if not validate_email(email):
            return abort(400, 'Invalid Email Address')
        if not fname or not lname or not fname.isalpha() or not lname.isalpha():
            return abort(400, "First and last name must be provided")
        if not password:
            return abort(400, "Password must be provided")

        user = User(email=email, fname=fname.capitalize(), lname=lname.capitalize(), password=password)

        try:
            check = user.save_user()
            if check:
                auth_token = user.generate_authentication_token()
                user_data = dict(data=marshal(user, USER))
                response = {
                    'status': 'success',
                    'message': 'Successfully Registered',
                    'auth_token': auth_token.decode('utf-8')
                }
                response.update(user_data)
                return response, 201
            else:
                response = {'status': 'fail', 'message': 'User Exists'}
                return response, 400
        except Exception as e:
            return abort(500, 'Error creating your account:{}'.format(e))


@auth_api.route('/login', endpoint='login')
class AuthenticateUser(Resource):
    """
    Handles requests for authentication of a user, based on the user's email
    and password
    """
    @auth_api.response(201, 'Login Successful')
    @auth_api.response(400, 'Bad Request')
    @auth_api.response(500, 'Internal Server Error')
    @auth_api.doc(model='login', body=LOGIN)
    def post(self):
        """
        Handles post requests for authentication of a user
        """
        post_data = request.get_json()
        email = strip_white_space(post_data.get('email'), skip_check_symbols=True)
        password = strip_white_space(post_data.get('password'))

        if not validate_email(email):
            return abort(400, 'Invalid Email Address')
        if not password:
            return abort(400, 'Password is required')

        user = User.query.filter_by(email=email).first()
        try:
            if user and user.verify_password(password):
                auth_token = user.generate_authentication_token()
                user_data = dict(data=marshal(user, USER))
                response = {
                    'status': 'success',
                    'message': 'Login Successful',
                    'auth_token': auth_token.decode('utf-8')
                }
                response.update(user_data)
                return response, 201
            response = {
                'status': 'fail',
                'message': 'Failed to authenticate user'
            }
            return response, 400
        except Exception as e:
            return abort(500, 'Error logging in user:{}'.format(e))


@auth_api.route('/logout', endpoint='logout')
class Logout(Resource):
    """
    This method logs the user out of the system
    """
    @auth_api.header('x-access-token', 'Access Token', required=True)
    @auth.login_required
    @auth_api.response(201, 'Logout Successful')
    def get(self):
        """
        Handles logout
        """
        try:
            token = request.headers.get('x-access-token')
            blacklist_token = BlackListToken(token=token)
            blacklist_token.save()
            g.current_user = None
            response = {
                'status': 'success',
                'message': 'Logout Successful'
            }
            return response, 201
        except Exception as e:
            return abort(500, 'Error logging out user:{}'.format(e))

    
