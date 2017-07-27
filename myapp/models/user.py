"""
Script contains the model for a user
"""
from .. import db

class User(db.Model):
    """
    Class used as a representation of the user model
    """
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, email, password):
        pass

