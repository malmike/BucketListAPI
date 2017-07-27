"""
This script is a base_test script that sets up the initial
configurations of the tests. It creates the flask test
environment in which the tests can run
"""
from flask_testing import TestCase

from instance import environments
from myapp import create_app, db

class BaseCase(TestCase):
    """
    This class is used to generate the default configurations for
    all the test file
    """
    def create_app(self):
        """
        Creates a flask instance for testing
        """
        return create_app(environments['testing'])

    def setUp(self):
        """
        Sets up the default configurations, and in this case creates
        the database to be used
        """
        db.create_all()

    def tearDown(self):
        """
        Removes the default configurations, and in this case deletes the
        database data and sessions in sqlalchemy after each test
        """
        db.session.remove()
        db.drop_all()
