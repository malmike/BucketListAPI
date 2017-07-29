"""
This script is a base_test script that sets up the initial
configurations of the tests. It creates the flask test
environment in which the tests can run
"""
from flask_testing import TestCase
from sqlalchemy import inspect

from instance import ENVIRONMENTS
from myapp import create_app, db
from myapp.models.user import User
from myapp.models.bucketlist import BucketList


class BaseCase(TestCase):
    """
    This class is used to generate the default configurations for
    all the test file
    """
    def create_app(self):
        """
        Creates a flask instance for testing
        """
        return create_app(ENVIRONMENTS['testing'])

    def setUp(self):
        """
        Sets up the default configurations, and in this case creates
        the database to be used
        """
        self.app = self.create_app()
        self.client = self.app.test_client
        with self.app.app_context():
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


    def add_test_users(self):
        """
        Method adds users to the database for testing
        """
        user = User(email='test@test.com', password='test')
        user2 = User(email='test2@test.com', password='test')
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()


    def add_test_bucketlists(self):
        """
        Method adds bucketlists to the database for testing
        """
        user = User()
        returned_user = user.query.filter_by(email='test@test.com').first()
        bucketlist = BucketList(user_id=returned_user.id, name='test_bucketlist')
        bucketlist2 = BucketList(user_id=returned_user.id, name='test_bucketlist2')
        db.session.add(bucketlist)
        db.session.add(bucketlist2)
        db.session.commit()


    def tearDown(self):
        """
        Removes the default configurations, and in this case deletes the
        database data and sessions in sqlalchemy after each test
        """
        db.session.remove()
        db.drop_all()


