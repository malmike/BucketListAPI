"""
Script contains the model for a user
"""
from .. import db, bcrypt, app

class User(db.Model):
    """
    Class used as a representation of the user model
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email = None, password = None):
        if email and password:
            self.email = email
            self.password = bcrypt.generate_password_hash(
                password, app.config.get('BCRYPT_LOG_ROUNDS')
            )


    def user_email_exists(self, email):
        """
        Method is used to verify that a user email exists in
        the database
        """
        pass

    def __repr__(self):
        return '<UserEmail %r>' % self.email

