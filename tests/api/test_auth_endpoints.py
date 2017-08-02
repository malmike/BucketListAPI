"""
File contains tests for the authentication endpoints like user authentication,
user registration, logout and user verification
"""
from unittest import TestCase
import json

from tests.base_case import BaseCase

class AuthEndPointsTests(BaseCase, TestCase):
    """
    Class contains tests for the authentication endpoints like user authentication,
    user registration, logout and user verification
    """
    def test_registration(self):
        """
        This method tests the user registration method
        """
        response = self.register_user("test@testing.com")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['message'], 'Successfully Registered')


    def test_user_already_registered(self):
        """
        This method tests that registration of the same user fails
        We will use user 'test@test.com' that was added by the populate_db
        method in the BaseCase class
        """
        response = self.register_user("test@test.com")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(result['message'], 'User Exists')


    def register_user(self, email):
        """
        Method is used to carry out user registration for testing
        """
        _pword = "test"
        return self.client.post(
            '/api/v1/auth/register',
            data=json.dumps({"email": email, "password": _pword}),
            content_type="application/json",
            follow_redirects=True
        )
