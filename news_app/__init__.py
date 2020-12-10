from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import Configurations

config = Configurations()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)

from news_app import routes