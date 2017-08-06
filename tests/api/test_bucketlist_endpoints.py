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
