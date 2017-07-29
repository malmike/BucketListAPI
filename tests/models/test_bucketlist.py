"""
Contains tests for the bucketlist model
"""
from unittest import TestCase
from tests.base_case import BaseCase
from myapp.models.bucketlist import BucketList
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
