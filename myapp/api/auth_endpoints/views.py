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

user = auth_api.model(
    'User',
    {
        'email':fields.String(required=True, description="User's Email", example="test@test.com"),
        'password':fields.String(required=True, description="User's Password", example="test_password")
    }
)

@auth_api.route('/register', endpoint='registration')
class RegisterUser(Resource):
    """
    Class contains mthods that handle requests for registering a new user
    """
    @auth_api.response(201, 'Successful User Registration')
    @auth_api.response(400, 'Request not understood by the server')
    @auth_api.response(409, 'User Data is invalid or User Exists')
    @auth_api.doc(model='User', body=user)
    def post(self):
        """
        Method receives post data used to register a new user
        """
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')

        if not self.__validate_email(email):
            return abort(409, 'Invalid Email Address')

        user = User(email=email,password=password)

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
            return abort(400, message='Error creating your account:{}'.format(e.message))


    @staticmethod
    def __validate_email(email):
        """
        Method validates that the email passed is valid
        regular expression used is got from http://emailregex.com
        """
        email_re = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return True if search(email_re, email) else False

