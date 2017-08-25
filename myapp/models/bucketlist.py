"""
Script contains the model for a bucketlist
"""

from .base_model import BaseModel, db
from .bucketlist_item import BucketListItem


class BucketList(BaseModel):
    """
    Class used as a representation of the bucketlist model
    """
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Use cascade='delete,all' to propagate the deletion of a User onto its Bucketlists
    bucketlist_items = db.relationship(
        BucketListItem, backref='bucketlist_item', uselist=True, cascade='delete,all'
    )


    def __item_exists(self, name, user_id):
        """
        Method is used to verify that a bucketlist name exists in
        the database
        """
        if BucketList.query.filter_by(user_id=user_id).filter(BucketList.name.ilike(name)).first():
            return True
        return False


    def save_bucketlist(self):
        """
        Method is used to add a bucketlist to the database
        """
        if self.__item_exists(self.name, self.user_id):
            return False
        self.add_data_set()
        return True


    def delete_bucketlist(self):
        """
        Method is used to add a bucketlist to the database
        """
        if not self.__item_exists(self.name, self.user_id):
            return False
        self.delete_data_set()
        return True


    def __repr__(self):
        return '<BucketList %r>' % self.name
