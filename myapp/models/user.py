"""
Script contains the model for a user
"""
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature, SignatureExpired
)
from flask_bcrypt import Bcrypt

from instance.config import Config
from .base_model import BaseModel, db
from .bucketlist import BucketList
from re import search


bcrypt = Bcrypt()

class User(BaseModel):
    """
    Class used as a representation of the user model
    """
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), index=True, nullable=False)
    _password = db.Column(db.String(255), nullable=False)
    # Use cascade='delete,all' to propagate the deletion of a User onto its Bucketlists
    bucketlists = db.relationship(
        BucketList, backref='user', uselist=True, cascade='delete,all'
    )


    @property
    def password(self):
        """
        Method that is run when password property is called
        """
        return "Password is only writable"


    @password.setter
    def password(self, password):
        """
        Method helps set the password property for the class
        """
        self._password = bcrypt.generate_password_hash(
            password, Config.BCRYPT_LOG_ROUNDS
        ).decode()


    @staticmethod
    def __item_exists(value):
        """
        Method verifies that a user email exists in the database
        """
        return True if User.query.filter_by(email=value).first() else False


    def verify_password(self, password):
        """
        Method is used to verify a users password matches the
        password passed
        """
        return bcrypt.check_password_hash(self._password, password)


    def save_user(self):
        """
        Method is used to add a user to the database
        """
        if not self.__item_exists(self.email):
            self.add_data_set()
            return True
        return False


    def delete_user(self):
        """
        Method is used to delete an existing user from the database
        """
        if self.__item_exists(self.email):
            self.delete_data_set()
            return True
        return False


    def generate_authentication_token(self, duration=Config.AUTH_TOKEN_DURATION):
        """
        Method for generating a JWT authentication token
        """
        serializer = Serializer(Config.SECRET_KEY, expires_in=int(duration))
        return serializer.dumps({"id":self.id})

    @staticmethod
    def verify_authentication_token(token):
        """
        Method is used to verify authentication token
        """
        serializer = Serializer(Config.SECRET_KEY)
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return False
        except BadSignature:
            return False
        return data['id'] if data['id'] else False


    def __repr__(self):
        return '<UserEmail %r>' % self.email
