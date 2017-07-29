"""
Script contains the model for a bucketlist
"""
from myapp import db
from datetime import datetime
import pytz

class BucketList(db.Model):
    """
    Class used as a representation of the user model
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created = db.Column(
        db.DateTime,
        default=datetime.now(tz=pytz.timezone('Africa/Kampala'))
    )
    modified = db.Column(
        db.DateTime,
        default=datetime.now(tz=pytz.timezone('Africa/Kampala')),
        onupdate=datetime.now(tz=pytz.timezone('Africa/Kampala'))
    )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __bucketlist_exists(self, name):
        """
        Method is used to verify that a bucketlist name exists in
        the database
        """
        return True if BucketList.query.filter_by(name=name).first() else False


    def add_bucketlist(self):
        """
        Method is used to add a user to the database
        """
        if not self.__bucketlist_exists(self.name):
            db.session.add(self)
            db.session.commit()
            return True
        return False
