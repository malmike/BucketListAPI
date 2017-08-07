"""
File contains tests for the bucketlist item endpoints
"""
from unittest import TestCase
import json
from datetime import date

from tests.base_case import BaseCase
from myapp.models.user import User
from myapp.models.bucketlist import BucketList
from myapp.models.bucketlist_item import BucketListItem

class BucketlistEndPointsTests(BaseCase, TestCase):
    """
    Class contains tests for the bucketlist endpoints
    """
    def test_get_bucketlist_items(self):
        """
        Method test the endpoint for getting bucketlist items
        For the user we will login using an existing user email:'test@test.com', password: 'test'
        We will check the number of items brought back to those when directly accessing the database
        """
        email = "test@test.com"
        _pword = "test"
        user = User.query.filter_by(email=email).first()
        bucketlist = BucketList.query.filter_by(user_id=user.id, id=1).first()
        items_no = len(bucketlist.bucketlist_items)
        headers = self.authentication_headers(email=email, password=_pword)
        response = self.client.get(
            '/api/v1/bucketlist/1/items/',
            content_type="application/json",
            headers=headers,
            follow_redirects=True
        )
        result = json.loads(response.data)
        self.assertEqual(len(result), items_no)


    def test_add_bucketlist_items(self):
        """
        Method test the endpoint for adding bucketlist item
        For the user we will login using an existing user email:'test@test.com', password: 'test'
        """
        email = "test@test.com"
        _pword = "test"
        user = User.query.filter_by(email=email).first()
        bucketlist = BucketList.query.filter_by(user_id=user.id, name="test_bucketlist").first()
        item_no = BucketListItem.query.filter_by(bucketlist_id=bucketlist.id).count()
        response = self.add_bucketlist_item(email, _pword, bucketlist.id)
        result = json.loads(response.data)
        self.assertEqual(response.status, '201 CREATED')
        self.assertEqual(result['message'], 'Bucket list item added')
        new_item_no = BucketListItem.query.filter_by(bucketlist_id=bucketlist.id).count()
        self.assertLess(item_no, new_item_no)


    def add_bucketlist_item(self, email, password, buckelist_id):
        """
        Method is used to send request to the api to add a bucketlist for testing
        """
        test_date = str(date(2020, 9, 22))
        headers = self.authentication_headers(email=email, password=password)
        return self.client.post(
            '/api/v1/bucketlist/{}/items/'.format(buckelist_id),
            data=json.dumps({"name": "bucketlist_item_name", "finished_by": test_date}),
            content_type="application/json",
            headers=headers,
            follow_redirects=True
        )
