"""
This script is a base_test script that sets up the initial
configurations of the tests. It creates the flask test
environment in which the tests can run
"""
from flask_testing import TestCase
from datetime import date
import json

from instance import ENVIRONMENTS
from manage import APP, db
from myapp.models.user import User
from myapp.models.bucketlist import BucketList
from myapp.models.bucketlist_item import BucketListItem


class BaseCase(TestCase):
    """
    This class is used to generate the default configurations for
    all the test file
    """
    @staticmethod
    def create_app():
        """
        Creates a flask instance for testing
        """
        return APP


    def setUp(self):
        """
        Sets up the default configurations, and in this case creates
        the database to be used
        """
        with self.app.test_client():
            db.session.close()
            db.drop_all()
            db.create_all()

        self.populate_db()


    def populate_db(self):
        """
        Method is used to populate the database with test data
        """
        self.add_test_users()
        self.add_test_bucketlists()
        self.add_test_bucketlist_items()


    @staticmethod
    def add_test_users():
        """
        Method adds users to the database for testing
        """
        _pword = "test"
        user = User(
            fname='Ftest',
            lname='Ltest',
            email='test@test.com',
            password=_pword
        )
        user2 = User(
            fname='Ftest2',
            lname='Ltest2',
            email='test2@test.com',
            password=_pword
        )
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()


    @staticmethod
    def add_test_bucketlists():
        """
        Method adds bucketlists to the database for testing
        """
        user = User.query.filter_by(email='test@test.com').first()
        bucketlist = BucketList(user_id=user.id, name='test_bucketlist')
        bucketlist2 = BucketList(user_id=user.id, name='test_bucketlist2')
        db.session.add(bucketlist)
        db.session.add(bucketlist2)
        db.session.commit()


    @staticmethod
    def add_test_bucketlist_items():
        """
        Method adds bucketlists items to the database for testing
        """
        bucketlist = BucketList.query.filter_by(name='test_bucketlist').first()
        item = BucketListItem(
            finished_by=date(2020, 8, 22),
            bucketlist_id=bucketlist.id,
            name='test_item'
        )
        item2 = BucketListItem(
            finished_by=date(2020, 9, 22),
            bucketlist_id=bucketlist.id,
            name='test_item2'
        )
        db.session.add(item)
        db.session.add(item2)
        db.session.commit()


    def post_user_data(self, path, data):
        """
        Method is used to send user data to the api basing on the
        path passed as an argument
        """
        return self.client.post(
            path,
            data=json.dumps(data),
            content_type="application/json",
            follow_redirects=True
        )


    def authentication_headers(self, email, password):
        """
        Method generates authentication headers for the test user
        basing on the email and password passed in the arguments
        """
        path = '/api/v1/auth/login'
        data = {"email": email, "password": password}
        response = self.post_user_data(path, data)
        result = json.loads(response.data.decode('utf-8'))
        self.assertTrue(result['auth_token'])
        return {'x-access-token': result['auth_token']}


    @staticmethod
    def tearDown():
        """
        Removes the default configurations, and in this case deletes the
        database data and sessions in sqlalchemy after each test
        """
        db.session.remove()
        db.drop_all()
