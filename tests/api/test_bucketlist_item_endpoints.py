"""
File contains tests for the bucketlist item endpoints
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
    def test_get_bucketlist_items(self):
        """
        Method test the endpoint for getting bucketlists
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
