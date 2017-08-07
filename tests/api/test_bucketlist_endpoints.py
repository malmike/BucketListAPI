"""
File contains tests for the bucketlist endpoints
"""
from unittest import TestCase
import json

from tests.base_case import BaseCase
from myapp.models.user import User
from myapp.models.bucketlist import BucketList

class BucketlistEndPointsTests(BaseCase, TestCase):
    """
    Class contains tests for the bucketlist endpoints
    """
    def test_add_bucketlist(self):
        """
        Method tests that the endpoint meant to add a bucketlist actually adds a bucketlist
        For the user we will login using an existing user email:'test@test.com', password: 'test'
        """
        email = "test@test.com"
        _pword = "test"
        user = User.query.filter_by(email=email).first()
        bucketlist_no = BucketList.query.filter_by(user_id=user.id).count()
        response = self.add_bucketlist(email, _pword, 'test_bucketlist_name')
        result = json.loads(response.data)
        self.assertEqual(response.status, '201 CREATED')
        self.assertEqual(result['message'], 'Bucketlist Added')
        new_bucketlist_no = BucketList.query.filter_by(user_id=user.id).count()
        self.assertNotEqual(bucketlist_no, new_bucketlist_no)


    def test_fail_repeated_buckelist(self):
        """
        Method tests that there can not be more than one bucketlist added with the
        same name. We will use one of the already existing bucketlist names 'test_bucketlist'
        For the user we will login using an existing user email:'test@test.com', password: 'test'
        """
        user = User.query.filter_by(email="test@test.com").first()
        bucketlist_no = BucketList.query.filter_by(user_id=user.id).count()
        response = self.add_bucketlist("test@test.com", "test", 'test_bucketlist')
        result = json.loads(response.data)
        self.assertEqual(response.status, '409 CONFLICT')
        self.assertEqual(result['message'], 'Bucketlist Exists')
        new_bucketlist_no = BucketList.query.filter_by(user_id=user.id).count()
        self.assertEqual(bucketlist_no, new_bucketlist_no)


    def test_get_bucketlists(self):
        """
        Method test the endpoint for getting bucketlists
        For the user we will login using an existing user email:'test@test.com', password: 'test'
        We will check the number of items brought back to those when directly accessing the database
        """
        email = "test@test.com"
        _pword = "test"
        user = User.query.filter_by(email=email).first()
        bucketlist_no = BucketList.query.filter_by(user_id=user.id).count()
        headers = self.authentication_headers(email=email, password=_pword)
        response = self.client.get(
            '/api/v1/bucketlist',
            content_type="application/json",
            headers=headers,
            follow_redirects=True
        )
        result = json.loads(response.data)
        self.assertEqual(len(result), bucketlist_no)


    def test_get_bucketlist(self):
        """
        Method tests the endpoint for getting a bucketlist when the bucketlist id is passed
        For the user we will login using an existing user email:'test@test.com', password: 'test'
        """
        email = "test@test.com"
        _pword = "test"
        user = User.query.filter_by(email=email).first()
        bucketlist = BucketList.query.filter_by(id=1).first()
        self.assertEqual(bucketlist.user_id, user.id)
        response = self.get_bucketlist(email, _pword, bucketlist.id)
        result = json.loads(response.data)
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('name'), bucketlist.name)


    def test_get_bucketlist_wrong_id(self):
        """
        Tests the endpoint for getting a bucketlist when the wrong id is passed returns an error
        For the user we will login using an existing user email:'test@test.com', password: 'test'
        """
        email = "test@test.com"
        _pword = "test"
        bucketlist = BucketList.query.filter_by(id=0).first()
        self.assertFalse(bucketlist)
        response = self.get_bucketlist(email, _pword, 0)
        result = json.loads(response.data)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(
            result['message'],
            'Bucketlist with ID {} not found in the database'.format(0)
        )


    def add_bucketlist(self, email, password, buckelist_name):
        """
        Method is used to send request to the api to add a bucketlist for testing
        """
        headers = self.authentication_headers(email=email, password=password)
        return self.client.post(
            '/api/v1/bucketlist',
            data=json.dumps({"name": buckelist_name}),
            content_type="application/json",
            headers=headers,
            follow_redirects=True
        )


    def test_put_bucketlist(self):
        """
        Method tests the endpoint for put bucketlist i.e alter bucketlist data
        For the user we will login using an existing user email:'test@test.com', password: 'test'
        """
        data = {"name": "new_bucketlist_name"}
        user = User.query.filter_by(email="test@test.com").first()
        bucketlist = BucketList.query.filter_by(id=1).first()
        name = bucketlist.name
        self.assertEqual(bucketlist.user_id, user.id)
        response = self.put_bucketlist("test@test.com", 'test', bucketlist.id, data)
        result = json.loads(response.data)
        self.assertIsInstance(result, dict)
        self.assertNotEqual(result.get('name'), name)


    def test_put_bucketlist_wrong_id(self):
        """
        Method tests the endpoint for put bucketlist when an incorrect id is passed
        For the user we will login using an existing user email:'test@test.com', password: 'test'
        """
        data = {"name": "new_bucketlist_name"}
        bucketlist = BucketList.query.filter_by(id=0).first()
        self.assertFalse(bucketlist)
        response = self.put_bucketlist("test@test.com", 'test', 0, data)
        result = json.loads(response.data)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(
            result['message'],
            'Bucketlist with ID {} not found in the database'.format(0)
        )


    def test_delete_bucketlist(self):
        """
        Method tests the endpoint for delete bucketlist
        For the user we will login using an existing user email:'test@test.com', password: 'test'
        """
        user = User.query.filter_by(email="test@test.com").first()
        bucketlist = BucketList.query.filter_by(id=1).first()
        id = bucketlist.id
        self.assertEqual(bucketlist.user_id, user.id)
        response = self.delete_bucketlist("test@test.com", 'test', bucketlist.id)
        result = json.loads(response.data)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(result.get('message'), 'Bucketlist with ID {} deleted'.format(id))
        self.assertFalse(BucketList.query.filter_by(id=1).first())


    def test_delete_bucketlist_wrong_id(self):
        """
        Tests the endpoint for delete bucketlist return error code 400 when wrong id is passed
        For the user we will login using an existing user email:'test@test.com', password: 'test'
        """
        response = self.delete_bucketlist("test@test.com", 'test', 0)
        result = json.loads(response.data)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(
            result['message'],
            'Bucketlist with ID {} not found in the database'.format(0)
        )


    def get_bucketlist(self, email, password, bucketlist_id):
        """
        Method is used to get a bucketlist basing on the id passed
        """
        headers = self.authentication_headers(email=email, password=password)
        return self.client.get(
            '/api/v1/bucketlist/{}'.format(bucketlist_id),
            content_type="application/json",
            headers=headers,
            follow_redirects=True
        )


    def get_argument_bucketlist(self, email, password, arg_type, arg_value):
        """
        Method is used to get a bucketlist basing on the id passed
        """
        headers = self.authentication_headers(email=email, password=password)
        return self.client.get(
            '/api/v1/bucketlist?{}={}'.format(arg_type, arg_value),
            content_type="application/json",
            headers=headers,
            follow_redirects=True
        )


    def put_bucketlist(self, email, password, bucketlist_id, data):
        """
        Method is used to test passing of put data for the bucketlist to the api
        """
        headers = self.authentication_headers(email=email, password=password)
        return self.client.put(
            '/api/v1/bucketlist/{}'.format(bucketlist_id),
            content_type="application/json",
            data=json.dumps(data),
            headers=headers,
            follow_redirects=True
        )


    def delete_bucketlist(self, email, password, bucketlist_id):
        """
        Method is used to request api to delete bucketlist basing on the id
        passed
        """
        headers = self.authentication_headers(email=email, password=password)
        return self.client.delete(
            '/api/v1/bucketlist/{}'.format(bucketlist_id),
            content_type="application/json",
            headers=headers,
            follow_redirects=True
        )

