"""
Contains tests for the user model
"""
from unittest import TestCase

from tests.base_case import BaseCase
from myapp.models.user import User

class UserTests(BaseCase, TestCase):
    """
    Class contains tests for the user model
    """
    def test_user_is_inserted_in_db(self):
        """
        Method checks that a user is added to the data
        """
        user = User.query.filter_by(id=1).first()
        self.assertEqual(
            user.email,
            "test@test.com",
            "User was not created"
        )


    def test_password_is_not_readable(self):
        """
        Method checks that password is not readable
        """
        user = User.query.filter_by(email="test@test.com").first()
        self.assertEqual(user.password, 'Password is only writable')


    def test_verify_password(self):
        """
        Method that checks that the password is for the specific user
        """
        user = User.query.filter_by(email="test@test.com").first()
        self.assertTrue(
            user.verify_password('test'),
            'Password, matches email so it should return true'
        )


    def test_wrong_password_false(self):
        """
        Method checks that a wrong password returns false
        """
        user = User.query.filter_by(email="test@test.com").first()
        self.assertFalse(
            user.verify_password('testing'),
            "Password doesnot match email so it should return false"
        )


    def test_add_user(self):
        """
        Method checks that add user method actually adds a user
        to the database
        """
        _pword = "test"
        user = User(email='test@adduser.com', password=_pword)
        check = user.add_user()
        self.assertTrue(check, "User should be added")
        self.assertTrue(
            user.id,
            "User doesnot contain id so he is not added to the db"
        )


    def test_no_repeated_users_added(self):
        """
        Method checks that add user method actually adds a user
        to the database
        """
        _pword = "test"
        user = User(email='test@test.com', password=_pword)
        check = user.add_user()
        self.assertFalse(check, "User should already exist")
        self.assertFalse(
            user.id,
            "User doesnot contain id so he is not added to the db"
        )


    def test_delete_user(self):
        """
        Method checks that a user can be deleted from the database
        """
        #retrieve a test user from the database
        user = User.query.filter_by(email="test2@test.com").first()
        self.assertTrue(user)

        #delete the user from the database
        user.delete_user()
        verify_user = User.query.filter_by(email="test2@test.com").first()
        self.assertFalse(
            verify_user,
            "User that is deleted should not exist in the database"
        )


    def test_bucketlist_list(self):
        """
        Method tests that the bucket list relation in the user model
        returns a list of bucketlists specific to that user
        """
        user = User.query.filter_by(email="test@test.com").first()
        self.assertTrue(isinstance(user.bucketlist, list))
