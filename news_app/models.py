from datetime import datetime
from news_app import db

class SavedNews(db.Model):
    """
    Model of the SavedNews Table.
    """
    id = db.Column(db.BigInteger, primary_key=True)
    headline = db.Column(db.String(), nullable=False)
    url = db.Column(db.String(), nullable=False, unique=True)
    image = db.Column(db.String(), nullable=False, default='default.jpg')
    shortDescription = db.Column(db.String())
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    savedDate = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"SavedNews('{self.id}', '{self.headline}, '{self.url})"