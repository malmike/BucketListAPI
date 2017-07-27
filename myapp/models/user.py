"""
Script contains the model for a user
"""
from .. import db

class User(db.Model):
    """
    Class used as a representation of the user model
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))

    def __init__(self, email, password):
        self.email = email
        self.password = password

