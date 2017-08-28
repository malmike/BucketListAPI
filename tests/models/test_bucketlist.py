"""
Contains tests for the bucketlist model
"""
from unittest import TestCase
from datetime import datetime

from tests.base_case import BaseCase
from myapp.models.bucketlist import BucketList
from myapp.models.user import User

class BucketListTests(BaseCase, TestCase):
    """
    Class contains tests for the bucketlist model
    """
    def test_bucketlist_inserted_in_db(self):
        """
        Method checks that a bucketlist is added to the data
        """
        bucketlist = BucketList.query.filter_by(id=1).first()
        self.assertEqual(bucketlist.name, "test bucketlist", "Name not added")
        self.assertEqual(bucketlist.user_id, 1, "User Id not added")
        self.assertTrue(isinstance(bucketlist.created, datetime))
        self.assertTrue(isinstance(bucketlist.modified, datetime))


    def test_add_bucketlist(self):
        """
        Method checks that add bucketlist method actually adds a bucketlist
        to the database
        """
        user = User.query.filter_by(email="test2@test.com").first()
        bucketlist = BucketList(name='test bucketlist3', user_id=user.id)
        check = bucketlist.save_bucketlist()
        self.assertTrue(check, "Bucketlist should be added")
        self.assertTrue(
            bucketlist.id,
            "BucketList doesnot contain id so has not been added to the db"
        )


    def test_no_repeat_bucketlist_names(self):
        """
        Method checks that add bucketlist method does not add bucketlist
        with repeated names
        """
        user = User.query.filter_by(email="test@test.com").first()
        bucketlist = BucketList(name='test bucketlist', user_id=user.id)
        check = bucketlist.save_bucketlist()
        self.assertFalse(check, "Bucketlist should not be added")
        self.assertFalse(
            bucketlist.id,
            "BucketList contains id so has been added to the db"
        )


    def test_delete_bucketlist(self):
        """
        Method checks that a bucketlist can be deleted from the database
        """
        #retrieve a test bucketlist from the database
        bucketlist = BucketList.query.filter_by(name="test bucketlist2").first()
        self.assertTrue(bucketlist)

        #delete the bucketlist from the database
        bucketlist.delete_bucketlist()
        verify_bucketlist = BucketList.query.filter_by(name="test bucketlist2").first()
        self.assertFalse(
            verify_bucketlist,
            "BucketList that is deleted should not exist in the database"
        )


    def test_bucketlist_item_list(self):
        """
        Method tests that the bucketlist item relation in the bucketlist model
        returns a list of bucketlist items specific to that bucketlist
        """
        bucketlist = BucketList.query.filter_by(name="test bucketlist").first()
        self.assertTrue(isinstance(bucketlist.bucketlist_items, list))

