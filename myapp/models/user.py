"""
Script contains the model for a user
"""
from myapp import db, bcrypt, app
from myapp.models.base_model import BaseModel
from myapp.models.bucketlist import BucketList

class User(BaseModel):
    """
    Class used as a representation of the user model
    """
    email = db.Column(db.String(50), index=True, nullable=False)
    _password = db.Column(db.String(255), nullable=False)
    # Use cascade='delete,all' to propagate the deletion of a User onto its Bucketlists
    bucketlist = db.relationship(
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
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()


    def __user_email_exists(self, email):
        """
        Method is used to verify that a user email exists in
        the database
        """
        return True if User.query.filter_by(email=email).first() else False


    def verify_password(self, password):
        """
        Method is used to verify a users password matches the
        password passed
        """
        return bcrypt.check_password_hash(self._password, password)


    def add_user(self):
        """
        Method is used to add a user to the database
        """
        if not self.__user_email_exists(self.email):
            self.add_data_set()
            return True
        return False


    def delete_user(self):
        """
        Method is used to delete an existing user from the database
        """
        if self.__user_email_exists(self.email):
            self.delete_data_set()
            return True
        return False


    def __repr__(self):
        return '<UserEmail %r>' % self.email
