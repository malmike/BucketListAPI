"""
Contains tests for the api utilities
"""
from unittest import TestCase

from tests.base_case import BaseCase
from myapp.utilities.Utilities import validate_email

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
