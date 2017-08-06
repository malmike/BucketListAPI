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
        Method tests that the endpoint meant to add a bucketlist actually
        adds a bucketlist
        """
        email = "test@test.com"
        _pword = "test"
        user = User.query.filter_by(email=email).first()
        bucketlist_no = BucketList.query.filter_by(user_id=user.id).count()
        response = self.add_bucketlist(email, _pword, user.id, 'test_bucketlist_name')
        result = json.loads(response.data)
        self.assertEqual(response.status, 201)
        self.assertEqual(result['message'], 'Bucketlist Added')
        new_bucketlist_no = BucketList.query.filter_by(user_id=user.id).count()
        self.assertNotEqual(bucketlist_no, new_bucketlist_no)


    def add_bucketlist(self, email, password, user_id, buckelist_name):
        """
        Method is used to send request to the api to add a bucketlist for testing
        """
        headers = self.authentication_headers(email=email, password=password)
        return self.client.post(
            '/api/v1/bucketlist',
            data=json.dumps({"name": buckelist_name, "created_by": user_id}),
            content_type="application/json",
            headers=headers,
            follow_redirects=True
        )
