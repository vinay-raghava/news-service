from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from news_app.settings import Configurations
from flask_bcrypt import Bcrypt

config = Configurations()
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)

from news_app import routes