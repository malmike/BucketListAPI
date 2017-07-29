"""
Script contains the model for a bucketlist
"""
from myapp import db
from myapp.models.base_model import BaseModel
from myapp.models.bucketlist_item import BucketListItem


class BucketList(BaseModel):
    """
    Class used as a representation of the bucketlist model
    """
    name = db.Column(db.String(150), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Use cascade='delete,all' to propagate the deletion of a User onto its Bucketlists
    bucketlist_item = db.relationship(
        BucketListItem, backref='bucketlist_item', uselist=True, cascade='delete,all'
    )


    @staticmethod
    def __item_exists(value):
        """
        Method is used to verify that a bucketlist name exists in
        the database
        """
        return True if BucketList.query.filter_by(name=value).first() else False


    def add_bucketlist(self):
        """
        Method is used to add a bucketlist to the database
        """
        if self.__item_exists(self.name):
            return False
        self.add_data_set()
        return True


    def delete_bucketlist(self):
        """
        Method is used to add a bucketlist to the database
        """
        if not self.__item_exists(self.name):
            return False
        self.delete_data_set()
        return True


    def __repr__(self):
        return '<BucketList %r>' % self.name
