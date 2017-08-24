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
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(result), items_no)


    def test_add_bucketlist_items(self):
        """
        Method test the endpoint for adding bucketlist item
        For the user we will login using an existing user email:'test@test.com', password: 'test'
        """
        email = "test@test.com"
        _pword = "test"
        user = User.query.filter_by(email=email).first()
        bucketlist = BucketList.query.filter_by(user_id=user.id, name="test bucketlist").first()
        item_no = BucketListItem.query.filter_by(bucketlist_id=bucketlist.id).count()
        response = self.add_bucketlist_item(email, _pword, bucketlist.id)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status, '201 CREATED')
        self.assertEqual(result['message'], 'Bucket list item added')
        new_item_no = BucketListItem.query.filter_by(bucketlist_id=bucketlist.id).count()
        self.assertLess(item_no, new_item_no)


    def test_put_bucketlist_item(self):
        """
        Method tests the end point for updating a bucket list item using put
        """
        data = {"name": "bucketlist item name", "completed": True}
        email = "test@test.com"
        _pword = "test"
        user = User.query.filter_by(email=email).first()
        bucketlist = BucketList.query.filter_by(user_id=user.id, name="test bucketlist").first()
        item = BucketListItem.query.filter_by(bucketlist_id=bucketlist.id, id=1).first()
        self.assertNotEqual(item.name, "bucketlist item name")
        self.assertFalse(item.completed)

        response = self.put_bucketlist_item(email, _pword, bucketlist.id, 1, data)
        result = json.loads(response.data.decode('utf-8'))
        item2 = BucketListItem.query.filter_by(bucketlist_id=bucketlist.id, id=1).first()
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(item2.name, "bucketlist item name")
        self.assertTrue(item2.completed)


    def test_put_item_wrong_id(self):
        """
        Method tests the error raised when end point for updating a bucket list item
        using put contains the wrong id
        """
        data = {"name": "bucketlist item name", "completed": True}
        email = "test@test.com"
        _pword = "test"
        user = User.query.filter_by(email=email).first()
        bucketlist = BucketList.query.filter_by(user_id=user.id, name="test bucketlist").first()
        item = BucketListItem.query.filter_by(bucketlist_id=bucketlist.id, id=0).first()
        self.assertFalse(item)

        response = self.put_bucketlist_item(email, _pword, bucketlist.id, 0, data)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(
            result['message'],
            'Bucketlist Item with ID {} not found in the database'.format(0)
        )


    def test_delete_bucketlist_item(self):
        """
        Method tests the request to delete a bucketlist item
        """
        email = "test@test.com"
        _pword = "test"
        user = User.query.filter_by(email=email).first()
        bucketlist = BucketList.query.filter_by(user_id=user.id, name="test bucketlist").first()
        item = BucketListItem.query.filter_by(bucketlist_id=bucketlist.id, id=1).first()
        self.assertTrue(item)

        response = self.delete_bucketlist_item(email, _pword, bucketlist.id, item.id)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(
            result['message'],
            'Bucketlist Item with ID {} deleted'.format(item.id)
        )
        item = BucketListItem.query.filter_by(bucketlist_id=bucketlist.id, id=1).first()
        self.assertFalse(item)


    def test_delete_item_wrong_id(self):
        """
        Method tests the error raised when end point for delete a bucket list item
        contains the wrong id
        """
        email = "test@test.com"
        _pword = "test"
        user = User.query.filter_by(email=email).first()
        bucketlist = BucketList.query.filter_by(user_id=user.id, name="test bucketlist").first()
        item = BucketListItem.query.filter_by(bucketlist_id=bucketlist.id, id=0).first()
        self.assertFalse(item)

        response = self.delete_bucketlist_item(email, _pword, bucketlist.id, 0)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(
            result['message'],
            'Bucketlist Item with ID {} not found in the database'.format(0)
        )


    def add_bucketlist_item(self, email, password, buckelist_id):
        """
        Method is used to send request to the api to add a bucketlist for testing
        """
        test_date = str(date(2020, 9, 22))
        headers = self.authentication_headers(email=email, password=password)
        return self.client.post(
            '/api/v1/bucketlist/{}/items/'.format(buckelist_id),
            data=json.dumps({"name": "bucketlist item name", "finished_by": test_date}),
            content_type="application/json",
            headers=headers,
            follow_redirects=True
        )


    def put_bucketlist_item(self, email, password, bucketlist_id, item_id, data):
        """
        Method is used to send request for put for the bucketlist item to the api
        """
        headers = self.authentication_headers(email=email, password=password)
        return self.client.put(
            '/api/v1/bucketlist/{}/items/{}'.format(bucketlist_id, item_id),
            content_type="application/json",
            data=json.dumps(data),
            headers=headers,
            follow_redirects=True
        )


    def delete_bucketlist_item(self, email, password, bucketlist_id, item_id):
        """
        Method is used to send request to delete a bucketlist item
        """
        headers = self.authentication_headers(email=email, password=password)
        return self.client.delete(
            '/api/v1/bucketlist/{}/items/{}'.format(bucketlist_id, item_id),
            content_type="application/json",
            headers=headers,
            follow_redirects=True
        )
