"""
Script contains the model for a bucketlist
"""
from .. import db

class BucketList(db.Model):
    """
    Class used as a representation of the user model
    """
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, user_id, bucketlist_name):
        pass

