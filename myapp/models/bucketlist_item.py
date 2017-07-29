"""
Script contains the model for a bucketlist items
"""
from datetime import datetime
import pytz

from myapp import db


class BucketListItem(db.Model):
    """
    Class used as a representation of the bucketlist item model
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    created = db.Column(
        db.DateTime,
        default=datetime.now(tz=pytz.timezone('Africa/Kampala'))
    )
    modified = db.Column(
        db.DateTime,
        default=datetime.now(tz=pytz.timezone('Africa/Kampala')),
        onupdate=datetime.now(tz=pytz.timezone('Africa/Kampala'))
    )
    finished_by = db.Column(
        db.Date,
        default=datetime.now(tz=pytz.timezone('Africa/Kampala'))
    )
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucket_list.id'), nullable=False)



    def add_bucketlist_item(self):
        """
        Method is used to add a bucketlist item to the database
        """
        db.session.add(self)
        db.session.commit()
        return True

