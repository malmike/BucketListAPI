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

    def test_that_user_table_is_created(self):
        """
        Method checks that the user table is created
        """
        user = User.query.filter_by(id=1).first()
        self.assertEqual(
            1,
            user.id,
            "No data addded, so the table is not created"
        )

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


    def test_password_is_encoded(self):
        """
        Method checks that password is encoded
        """
        user = User.query.filter_by(email="test@test.com").first()
        self.assertNotEqual(user.password, 'test')


    def test_encoding_not_similar(self):
        """
        Method that checks that the password is encoded
        before storing in the database
        """
        user_test = User('test@test.com', 'test')
        user = User.query.filter_by(email="test@test.com").first()
        self.assertNotEqual(user.password, user_test.password)


    def test_that_email_exists(self):
        """
        Method checks that method to verify if an email exists in the
        database returns true
        """
        user = User()
        check = user.user_email_exists("test@test.com")
        self.assertTrue(check)


    def test_that_email_doesnot_exists(self):
        """
        Method checks that method to verify if an email doesnot exists in the
        database returns false
        """
        user = User()
        check = user.user_email_exists("test@testing.com")
        self.assertFalse(check)