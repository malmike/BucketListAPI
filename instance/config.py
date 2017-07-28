"""
The script contains the configurations for the bucket list api
application
"""
import os

class Config(object):
    """
    Contains the default configurations for the app
    """
    DEBUG = False
    TESTING = False
    SECRET = os.getenv('SECRET') or 'KJI38US783KJW92MOYHSYE4837HNFYNE8347SH873UD384UFYHE'
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/bucketlist_api_dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """
    Contains the development configurations for the application
    """
    DEBUG = True


class TestConfig(Config):
    """
    Contains the configurations used while testing the application
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/test_db"


class ProductionConfig(Config):
    """
    Contains configurations for the production environment
    """
    DEBUG = False
    TESTING = False
