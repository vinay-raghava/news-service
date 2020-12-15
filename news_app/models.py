import jwt
from datetime import datetime, timedelta
from news_app import db, config

class User(db.Model):
    """
    Model of the User table.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique = True)
    password = db.Column(db.String(), nullable=False)
    joinedDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    savedNews = db.relationship('SavedNews', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email})"
    @property
    def serialize(self):
        """
        Returns the object data in serializable format
        """
        return {
            'username': self.username,
            'email': self.email,
            'joinedDate': self.joinedDate
        }

    def generateAuthToken(self):
        """
        Generates an auth token for the given user id.
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, minutes=30),
                'iat': datetime.utcnow(),
                'sub': self.id
            }
            return jwt.encode(payload, config.SECRET_KEY, algorithm='HS256').decode()
        except Exception as error:
            print(error)
            return error
    @staticmethod
    def decodeAuthToken(authToken):
        """
        Decodes the auth token
        """
        try:
            return jwt.decode(authToken, config.SECRET_KEY, algorithm='HS256')['sub']
        except jwt.ExpiredSignatureError:
            return 'signature expired, Please login again'
        except jwt.InvalidTokenError:
            return 'Invalid token'


class SavedNews(db.Model):
    """
    Model of the SavedNews Table.
    """
    id = db.Column(db.BigInteger, primary_key=True)
    headline = db.Column(db.String(), nullable=False)
    url = db.Column(db.String(), nullable=False, unique=True)
    image = db.Column(db.String(), nullable=False, default='default-news-image.png')
    shortDescription = db.Column(db.String())
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    savedDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"SavedNews('{self.id}', '{self.headline}, '{self.url})"

    @property
    def serialize(self):
        """
        Returns the Saved news object data in serializable format
        """
        return {
            "id": self.id,
            "headline": self.headline,
            "url": self.url,
            "image": self.image,
            "shortDescription": self.shortDescription,
            "saved": True,
            "date": self.date,
            "savedDate": self.savedDate
        }