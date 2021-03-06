"""
File contains tests for the authentication endpoints like user authentication,
user registration, logout and user verification
"""
from unittest import TestCase
from myapp.models.blacklist_token import BlackListToken
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
        data = {"email": "test@testing.com", "password":"test", "fname": 'Fname', "lname": "Lname"}
        response = self.post_user_data(path=path, data=data)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['message'], 'Successfully Registered')
        self.assertIsInstance(result['data'], dict)


    def test_user_already_registered(self):
        """
        This method tests that registration of the same user fails
        We will use user 'test@test.com' that was added by the populate_db
        method in the BaseCase class
        """
        path = '/api/v1/auth/register'
        data = {"email": "test@test.com", "password": "test", "fname": 'Fname', "lname": "Lname"}
        response = self.post_user_data(path=path, data=data)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 409)
        self.assertEqual(result['message'], 'User Exists')


    def test_invalid_email(self):
        """
        This method tests that an Invalid Email Address is not
        registered
        """
        path = '/api/v1/auth/register'
        data = {"email": "testtest.com", "password": "test", "fname": 'Fname', "lname": "Lname"}
        response = self.post_user_data(path=path, data=data)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['message'], 'Invalid Email Address')


    def test_authenticate_valid_user(self):
        """
        This method is used to test the user authentication method
        basing on the email and password passed
        We will use user 'test@test.com' that was added by the populate_db
        method in the BaseCase class
        """
        path = '/api/v1/auth/login'
        data = {"email": "test@test.com", "password": "test"}
        response = self.post_user_data(path=path, data=data)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['message'], 'Login Successful')
        self.assertIsInstance(result['data'], dict)


    def test_non_existant_email(self):
        """
        This method is used to test the user authentication when email
        passed doesnot exists
        """
        path = '/api/v1/auth/login'
        data = {"email": "nonexitant@email.com", "password": "test"}
        response = self.post_user_data(path=path, data=data)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result['message'], 'Failed to authenticate user')


    def test_incorrect_password(self):
        """
        This method tests that authentication fails when the password passed
        is incorrect
        """
        path = '/api/v1/auth/login'
        data = {"email": "test@test.com", "password": "wrongpassword"}
        response = self.post_user_data(path=path, data=data)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result['message'], 'Failed to authenticate user')


    def test_logout(self):
        """
        This method tests that the logout function works
        """
        path = '/api/v1/auth/login'
        email = "test@test.com"
        pword = "test"
        data = {"email": email, "password": pword}
        response = self.post_user_data(path=path, data=data)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        headers = self.authentication_headers(email=email, password=pword)
        blacklist_no = BlackListToken.query.filter_by().count()
        response = self.client.get(
            '/api/v1/auth/logout',
            content_type="application/json",
            headers=headers,
            follow_redirects=True
        )
        new_blacklist_no = BlackListToken.query.filter_by().count()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['message'], 'Logout Successful')
        self.assertNotEqual(blacklist_no, new_blacklist_no)

        # TRY REACCESSING THE LOGOUT PATH
        response = self.client.get(
            '/api/v1/auth/logout',
            content_type="application/json",
            headers=headers,
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 401)
        

