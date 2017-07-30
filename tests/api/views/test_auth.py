"""
Contains tests for the user view that constitute those
of user registaation and user authententication
"""
from unittest import TestCase

from tests.base_case import BaseCase

class UserViewTests(BaseCase, TestCase):
    """
    Class contains tests for the user views that constitute
    those of user registration and user authentication
    """

    def test_user_registration(self):
        """
        Contains test for user registration method
        """