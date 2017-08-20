"""
This file contains the endpoints for authentication
i.e user registration, user authentication, user verification
and logout
"""
from flask_restplus import Namespace, Resource, abort, fields, marshal
from flask import request, g
from re import search
from myapp.models.user import User
from myapp.utilities.Utilities import validate_email

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
    @auth_api.response(400, 'Bad Request')
    @auth_api.response(500,'Internal Server Error')
    @auth_api.doc(model='User', body=USER)
    def post(self):
        """
        Handles post requests for registration of a new user
        """
        post_data = request.get_json()
        fname = post_data.get('fname') or None
        lname = post_data.get('lname') or None
        email = post_data.get('email')
        password = post_data.get('password')

        if not validate_email(email):
            return abort(400, 'Invalid Email Address')
        if not fname or not lname:
            return abort(400, "First and last name must be provided")

        user = User(email=email, fname=fname, lname=lname, password=password)

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
            return abort(500, 'Error creating your account:{}'.format(e.message))


@auth_api.route('/login', endpoint='login')
class AuthenticateUser(Resource):
    """
    Handles requests for authentication of a user, based on the user's email
    and password
    """
    @auth_api.response(201, 'Login Successful')
    @auth_api.response(400, 'Bad Request')
    @auth_api.response(500, 'Internal Server Error')
    @auth_api.doc(model='User', body=USER)
    def post(self):
        """
        Handles post requests for authentication of a user
        """
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')

        if not validate_email(email):
            return abort(400, 'Invalid Email Address')

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
            return abort(500, 'Error logging in user:{}'.format(e.message))
