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
