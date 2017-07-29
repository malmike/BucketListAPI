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


    def __bucketlist_exists(self, name):
        """
        Method is used to verify that a bucketlist name exists in
        the database
        """
        return True if BucketList.query.filter_by(name=name).first() else False


    def add_bucketlist(self):
        """
        Method is used to add a bucketlist to the database
        """
        if not self.__bucketlist_exists(self.name):
            self.add_data_set()
            return True
        return False


    def delete_bucketlist(self):
        """
        Method is used to add a bucketlist to the database
        """
        if self.__bucketlist_exists(self.name):
            self.delete_data_set()
            return True
        return False


    def __repr__(self):
        return '<BucketList %r>' % self.name
