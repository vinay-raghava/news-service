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
    savedNews = db.relationship('SavedNews', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email})"

    def generateAuthToken(self, user_id):
        """
        Generates an auth token for the given user id.
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
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
    image = db.Column(db.String(), nullable=False, default='default.jpg')
    shortDescription = db.Column(db.String())
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    savedDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"SavedNews('{self.id}', '{self.headline}, '{self.url})"