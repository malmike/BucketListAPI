"""
Contains tests for the bucketlist item model
"""
from unittest import TestCase
from datetime import datetime
from datetime import date

from tests.base_case import BaseCase
from myapp.models.bucketlist import BucketList
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
        self.assertEqual(item.name, "test item", "Name not added")
        self.assertEqual(item.bucketlist_id, 1, "User Id not added")
        self.assertTrue(isinstance(item.created, datetime))
        self.assertTrue(isinstance(item.modified, datetime))
        self.assertTrue(isinstance(item.finished_by, date))


    def test_add_bucketlist_item(self):
        """
        Method checks that add bucketlist item method actually adds a bucketlist
        item to the database
        """
        bucketlist = BucketList.query.filter_by(name="test bucketlist").first()
        item = BucketListItem(
            name='test item3',
            bucketlist_id=bucketlist.id,
            finished_by=date(2020, 9, 22)
        )
        check = item.save_bucketlist_item()
        self.assertTrue(check, "Bucketlist item should be added")
        self.assertTrue(
            item.id,
            "BucketList Item doesnot contain id so has not been added to the db"
        )


    def test_repeat_bucketlist_item(self):
        """
        Method checks that add bucketlist item method actually adds a bucketlist
        item to the database
        """
        bucketlist = BucketList.query.filter_by(name="test bucketlist").first()
        item = BucketListItem(
            name='test item',
            bucketlist_id=bucketlist.id,
            finished_by=date(2020, 9, 22)
        )
        check = item.save_bucketlist_item()
        self.assertFalse(check, "Bucketlist item should not be added")
        self.assertFalse(
            item.id,
            "BucketList Item doesnot contain id so has not been added to the db"
        )


    def test_delete_bucketlist_item(self):
        """
        Method checks that a bucketlist item can be deleted from the database
        """
        #retrieve a test bucketlist from the database
        item = BucketListItem.query.filter_by(id=1).first()
        self.assertTrue(item)

        #delete the bucketlist from the database
        item.delete_bucketlist_item()
        verify_item = BucketListItem.query.filter_by(id=1).first()
        self.assertFalse(
            verify_item,
            "BucketList item that is deleted should not exist in the database"
        )
