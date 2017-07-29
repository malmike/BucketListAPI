"""
Contains tests for the bucketlist model
"""
from unittest import TestCase
from tests.base_case import BaseCase
from myapp.models.bucketlist import BucketList
from myapp.models.user import User
from datetime import datetime

class BucketListTests(BaseCase, TestCase):
    """
    Class contains tests for the user model
    """
    def test_bucketlist_is_inserted_in_db(self):
        """
        Method checks that a user is added to the data
        """
        bucketlist = BucketList.query.filter_by(id=1).first()
        self.assertEqual(bucketlist.name, "test_bucketlist", "Name not added")
        self.assertEqual(bucketlist.user_id, 1, "User Id not added")
        self.assertTrue(isinstance(bucketlist.created, datetime))
        self.assertTrue(isinstance(bucketlist.modified, datetime))


    def test_add_bucketlist(self):
        """
        Method checks that add bucketlist method actually adds a bucketlist
        to the database
        """
        user = User.query.filter_by(email="test2@test.com").first()
        bucketlist = BucketList(name='test_bucketlist3', user_id=user.id)
        check = bucketlist.add_bucketlist()
        self.assertTrue(check, "Bucket should be added")
        self.assertTrue(
            bucketlist.id,
            "BucketList doesnot contain id so has not been added to the db"
        )


    def test_no_repeat_bucketlist_names(self):
        """
        Method checks that add bucketlist method actually adds a bucketlist
        to the database
        """
        user = User.query.filter_by(email="test@test.com").first()
        bucketlist = BucketList(name='test_bucketlist', user_id=user.id)
        check = bucketlist.add_bucketlist()
        self.assertFalse(check, "Bucket should be added")
        self.assertFalse(
            bucketlist.id,
            "BucketList contains id so has been added to the db"
        )
