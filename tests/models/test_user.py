"""
Contains tests for the user model
"""
from tests.base_case import BaseCase

from myapp import db
from myapp.models.user import User

class UserTests(BaseCase):
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

    def test_that_user_is_inserted_in_db(self):
        """
        Method checks that a user is added to the data
        """
        user = User.query.filter_by(id=1).first()
        self.assertEqual(
            user.email,
            "test@test.com",
            "User was not created"
        )
