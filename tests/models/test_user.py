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
        user = User('test@test.com', 'test')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(
            1, user.id,
            "No data addded, so the table is not created"
        )
