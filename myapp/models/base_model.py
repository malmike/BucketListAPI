"""
Script contains the base model from which other models will inherit
"""
from datetime import datetime
import pytz

from myapp import db


class BaseModel(db.Model):
    """
    Class contains the base model from which other models will inherit
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(
        db.DateTime,
        default=datetime.now(tz=pytz.timezone('Africa/Kampala'))
    )
    modified = db.Column(
        db.DateTime,
        default=datetime.now(tz=pytz.timezone('Africa/Kampala')),
        onupdate=datetime.now(tz=pytz.timezone('Africa/Kampala'))
    )


    def add_data_set(self):
        """
        Method is used to add a data set to the database
        """
        db.session.add(self)
        db.session.commit()


    def delete_data_set(self):
        """
        Method is used to delete an existing dataset from the database
        """
        db.session.delete(self)
        db.session.commit()


    __isabstractmethod__=True
    @staticmethod
    def __item_exists():
        return
