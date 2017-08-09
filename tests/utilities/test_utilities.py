"""
Contains tests for the api utilities
"""
from unittest import TestCase
import json

from tests.base_case import BaseCase
from myapp.utilities.Utilities import validate_email, verify_token


class UserTests(BaseCase, TestCase):
    """
    Class contains tests for the api utilities
    """
    def test_valid_email(self):
        """
        Tests that when a vaild email is passed, validate_email method
        returns true
        """
        self.assertTrue(validate_email('test@test.com'))


    def test_invalid_email(self):
        """
        Ensures that when one enters an invalid email, validate_email method
        returns false
        """
        self.assertFalse(validate_email('testtests.com'))


    def test_validate_token(self):
        """
        Tests the verify_token method in the utilities file
        """
        path = '/api/v1/auth/login'
        data = data = {"email": "test@test.com", "password":"test"}
        response = self.post_user_data(path=path, data=data)
        result = json.loads(response.data)
        self.assertTrue(result['auth_token'])
        self.assertTrue(
            verify_token(result['auth_token'])
        )
