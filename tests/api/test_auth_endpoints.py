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
        path = '/api/v1/auth/register'
        response = self.post_user_data(path=path, email="test@testing.com")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['message'], 'Successfully Registered')


    def test_user_already_registered(self):
        """
        This method tests that registration of the same user fails
        We will use user 'test@test.com' that was added by the populate_db
        method in the BaseCase class
        """
        path = '/api/v1/auth/register'
        response = self.post_user_data(path=path, email="test@test.com")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(result['message'], 'User Exists')


    def test_invalid_email(self):
        """
        This method tests that an Invalid Email Address is not
        registered
        """
        path = '/api/v1/auth/register'
        response = self.post_user_data(path=path, email="testtest.com")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(result['message'], 'Invalid Email Address')


    def test_authenticate_valid_user(self):
        """
        This method is used to test the user authentication method
        basing on the email and password passed
        We will use user 'test@test.com' that was added by the populate_db
        method in the BaseCase class
        """
        path = '/api/v1/auth/login'
        response = self.post_user_data(path=path, email="test@test.com", _pword="test")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['message'], 'Login Successful')


    def test_non_existant_email(self):
        """
        This method is used to test the user authentication when email
        passed doesnot exists
        """
        path = '/api/v1/auth/login'
        response = self.post_user_data(path=path, email="nonexitant@email.com", _pword="test")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result['message'], 'Failed to authenticate user')


    def test_incorrect_password(self):
        """
        This method tests that authentication fails when the password passed
        is incorrect
        """
        path = '/api/v1/auth/login'
        response = self.post_user_data(path=path, email="test@test.com", _pword="wrong_pword")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result['message'], 'Failed to authenticate user')
