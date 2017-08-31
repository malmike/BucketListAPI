"""
Script contains test that verify the app configurations
"""
from flask_testing import TestCase

from instance import ENVIRONMENTS
from myapp import create_app


class DevelopmentConfigTests(TestCase):
    """
    Class contains test that verify the app created with
    development configurations
    """
    @staticmethod
    def create_app():
        """
        Creates a flask instance for specific for development
        """
        return create_app(ENVIRONMENTS['development'])


    def setUp(self):
        """
        Sets up the default configurations
        """
        self.app = self.create_app()


    def test_app_is_development(self):
        """
        Tests that app was started with development settings
        """
        self.assertTrue(self.app.config['DEBUG'])
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'],
            "postgresql://localhost/bucketlist_api_dev"
        )



class TestingConfigTests(TestCase):
    """
    Class contains test that verify the app created with
    testing configurations
    """
    @staticmethod
    def create_app():
        """
        Creates a flask instance for specific for testing
        """
        return create_app(ENVIRONMENTS['testing'])


    def setUp(self):
        """
        Sets up the default configurations
        """
        self.app = self.create_app()


    def test_app_is_testing(self):
        """
        Tests that app was started with testing settings
        """
        self.assertTrue(self.app.config['DEBUG'])
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'],
            "postgresql://localhost/test_db"
        )
        