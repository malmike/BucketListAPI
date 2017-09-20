"""
Script contains a model for the blacklist tokens
"""
from .base_model import db

class BlackListToken(db.Model):
    """
    Class contains a model for blacklist tokens
    """
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)

    @staticmethod
    def check_blacklist(token):
        return BlackListToken.query.filter_by(token=str(token)).first()

    def save(self):
        """
        Method is used to add a data set to the database
        """
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return '<Token %r>' % self.token
    