"""
This file contains the endpoints for authentication
i.e user registration, user authentication, user verification
and logout
"""
from flask_restplus import Resource, abort
from flask import request
from re import search
from myapp.models.user import User

class RegisterUser(Resource):
    """
    Class contains mthods that handle requests for registering a new user
    """
    def post(self):
        """
        Method receives post data used to register a new user
        """
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')

        if not self.__validate_email(email):
            return abort(401, 'Invalid Email Address')

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
            return abort(401, message='Error creating your account:{}'.format(e.message))


    @staticmethod
    def __validate_email(email):
        """
        Method validates that the email passed is valid
        regular expression used is got from http://emailregex.com
        """
        email_re = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return True if search(email_re, email) else False

