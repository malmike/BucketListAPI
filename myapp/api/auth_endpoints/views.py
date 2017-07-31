"""
This file contains the endpoints for authentication
i.e user registration, user authentication, user verification
and logout
"""
from flask_restplus import Resource

class RegisterUser(Resource):
    """
    Class contains mthods that handle requests for registering a new user
    """
    def post(self):
        """
        Method receives post data used to register a new user
        """
        pass