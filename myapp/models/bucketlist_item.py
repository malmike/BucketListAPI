"""
Script contains the model for a bucketlist items
"""
from datetime import datetime
import pytz

from .base_model import BaseModel, db


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


    def __item_exists(self, item, bucketlist_id):
        """
        Method is used to verify that a bucketlist name exists in
        the database
        """
        if BucketListItem.query.filter_by(bucketlist_id=bucketlist_id).filter(BucketListItem.name.ilike(item)).first():
            return True
        return False


    def save_bucketlist_item(self):
        """
        Method is used to add a bucketlist item to the database
        """
        if self.__item_exists(self.name, self.bucketlist_id):
            return False
        self.add_data_set()
        return True


    def delete_bucketlist_item(self):
        """
        Method is used to add a bucketlist item to the database
        """
        if not self.__item_exists(self.name, self.bucketlist_id):
            return False
        self.delete_data_set()
        return True

