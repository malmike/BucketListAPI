"""
Contains tests for the bucketlist item model
"""
from unittest import TestCase
from datetime import datetime
from datetime import date
from tests.base_case import BaseCase
from myapp.models.bucketlist_item import BucketListItem


class BucketListItemTests(BaseCase, TestCase):
    """
    Class contains tests for the bucketlist item model
    """
    def test_item_is_inserted_in_db(self):
        """
        Method checks that a bucketlist item is added to the database
        """
        item = BucketListItem.query.filter_by(id=1).first()
        self.assertEqual(item.name, "test_item", "Name not added")
        self.assertEqual(item.bucketlist_id, 1, "User Id not added")
        self.assertTrue(isinstance(item.created, datetime))
        self.assertTrue(isinstance(item.modified, datetime))
        self.assertTrue(isinstance(item.finished_by, date))