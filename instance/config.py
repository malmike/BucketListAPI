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
    BCRYPT_LOG_ROUNDS = 13
    __secret_key = 'uMhwMM2q9L2Cg6kgTv2PFz7AbAUOsmMHuZCcwO0A7j6AdtzHuxAf9ctIUBZ4T0ea'
    SECRET_KEY = os.getenv('SECRET_KEY') or __secret_key
    AUTH_TOKEN_DURATION = os.getenv('TOKEN_DURATION') or 300
    __dbname = "postgresql://localhost/bucketlist_api_dev"
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_NAME') or __dbname
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """
    Contains the development configurations for the application
    """
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4


class TestConfig(Config):
    """
    Contains the configurations used while testing the application
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/test_db"
    BCRYPT_LOG_ROUNDS = 4


class ProductionConfig(Config):
    """
    Contains configurations for the production environment
    """
    DEBUG = False
    TESTING = False
