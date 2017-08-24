"""
Contains tests for the api utilities
"""
from unittest import TestCase
import json

from tests.base_case import BaseCase
from myapp.utilities.Utilities import validate_email, verify_token
from myapp.utilities.Utilities import check_for_symbols, strip_white_space


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
        result = json.loads(response.data.decode('utf-8'))
        self.assertTrue(result['auth_token'])
        self.assertTrue(
            verify_token(result['auth_token'])
        )

    
    def test_strip_white_space(self):
        """
        Tests that white space is trimmed off string passed to strip white
        space method
        """
        self.assertEqual(strip_white_space("  testing  "), "testing")
    

    def test_strip_white_space_return_false(self):
        """
        Tests that if only spaces are passed to the strip white space method
        false is returned
        """
        self.assertFalse(strip_white_space("    "))


    def test_string_contain_symbols(self):
        """
        Tests that when a string containing symbols is passed to the strip white
        space method, false is returned
        """
        self.assertFalse(strip_white_space("This is a bucket |!$t"))


    def test_check_for_symbols(self):
        """
        Tests that if a string or sentence is passed containing symbols, the
        return will be false and true if there are no symbols, and also returns 
        true when the boolean argument passed is true
        """
        self.assertFalse(check_for_symbols("The bucket |!$t", False))
        self.assertTrue(check_for_symbols("This bucket list", False))
        self.assertTrue(check_for_symbols("john@doe.com", True))
