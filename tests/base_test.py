"""
This script is a base_test script that sets up the initial
configurations of the tests. It creates the flask test
environment in which the tests can run
"""
from flask_testing import TestCase

from instance import environments
from myapp import create_app, db

class BaseTest(TestCase):

    def create_app(self):
        self.app = create_app(environments['testing'])
        return self.app

    def setUp(self):
        db.create_all()


    def test_app_is_created(self):
        self.assertTrue(self.app.config['DEBUG'])
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'] == "postgresql://root:root@localhost/test_db",
            "Database configurations not setup"
            )

    def tearDown(self):
        db.session.remove()
        db.drop_all()
