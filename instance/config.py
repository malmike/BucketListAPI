"""
The script contains the configurations for the bucket list api
application
"""
class Config(object):
    """
    Contains the default configurations for the app
    """
    DEBUG = False
    TESTING = False
    SECRET = 'KJI38US783KJW92MOYHSYE4837HNFYNE8347SH873UD384UFYHE'
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
    CC_TEST_REPORTER_ID = "392653690efc9e65af92588e76d5d83f4c5660d20ee402b591b7df0035b60b7d"


class ProductionConfig(Config):
    """
    Contains configurations for the production environment
    """
    DEBUG = False
    TESTING = False
