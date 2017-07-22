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
    SECRET = 'KJI38US783KJW92MOY'
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/bucketlist_api"


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
