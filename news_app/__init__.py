from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from news_app.settings import Configurations
from flask_bcrypt import Bcrypt

config = Configurations()
db = SQLAlchemy()
bcrypt=Bcrypt()

def create_app(config=config):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['NEWS_API_KEY'] = config.NEWS_API_KEY

    db.init_app(app)
    bcrypt.init_app(app)

    from news_app.users.routes import users
    from news_app.news.routes import news

    app.register_blueprint(users)
    app.register_blueprint(news)

    return app