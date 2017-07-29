"""
Script contains the model for a bucketlist items
"""
from datetime import datetime
import pytz

from myapp import db
from myapp.models.base_model import BaseModel


class BucketListItem(BaseModel):
    """
    Class used as a representation of the bucketlist item model
    """
    name = db.Column(db.Text, nullable=False)
    finished_by = db.Column(
        db.Date,
        default=datetime.now(tz=pytz.timezone('Africa/Kampala'))
    )
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucket_list.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)


    def add_bucketlist_item(self):
        """
        Method is used to add a bucketlist item to the database
        """
        self.add_data_set()
        return True


    def delete_bucketlist_item(self):
        """
        Method is used to add a bucketlist item to the database
        """
        self.delete_data_set()
        db.session.commit()
        return True

