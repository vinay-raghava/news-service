import os
class Configurations():
    def __init__(self):
        self.NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
        self.SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
        self.SECRET_KEY = os.environ.get('SECRET_KEY')