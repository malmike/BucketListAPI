"""
Contains tests for the user model
"""
from unittest import TestCase
from time import sleep

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


    def test_token_generation(self):
        """
        Method tests that the generate token method returns a token
        """
        token = self.create_token()['token']
        self.assertTrue(isinstance(token, bytes))


    def test_decode_token(self):
        """
        Tests that the token created can be decoded
        """
        token_values = self.create_token()
        self.assertTrue(
            token_values['user'].verify_authentication_token(token_values['token'])
        )


    def test_token_expiration(self):
        """
        Should expect false when the token expires
        """
        token_values = self.create_token(duration=0.5, sleep_time=1)
        self.assertFalse(
            token_values['user'].verify_authentication_token(token_values['token'])
        )


    def test_token_aulteration(self):
        """
        Method should expect a false due to aulteration of the
        authentication token
        """
        token_values = self.create_token()
        a = 'a'.encode('utf-8')
        token = token_values['token'] + a
        self.assertFalse(
            token_values['user'].verify_authentication_token(token)
        )


    def test_token_distinct(self):
        """
        Tests that a token is distinct i.e can not generate the
        same token after token expiry
        """
        token1 = self.create_token(duration=0.5, sleep_time=1)['token']
        token2 = self.create_token(duration=0.5)['token']
        self.assertNotEqual(token1, token2)


    def create_token(self, duration=300, sleep_time=0):
        """
        Method is used to call the generate_authentication_token
        and returns a token
        """
        user = User.query.filter_by(email="test@test.com").first()
        token = user.generate_authentication_token(duration=duration)
        sleep(sleep_time)
        return {"user": user, "token":token}
