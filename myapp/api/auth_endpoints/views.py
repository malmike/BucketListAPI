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
    

    @staticmethod
    def __validate_email(email):
        """
        Method validates that the email passed is valid
        regular expression used is got from http://emailregex.com
        """
        email_re = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return True if search(email_re, email) else False

