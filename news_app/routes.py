import http.client
import uuid
import os
from dateutil.parser import parse
from flask_cors import cross_origin
from flask import request, jsonify, url_for, send_file
from news_app import app, db, config, bcrypt
from news_app.models import User, SavedNews
from news_app.utils.latest_news_getter import get_latest_news
from news_app.utils.check_authorization import isUserAuthorized

API_KEY = config.NEWS_API_KEY

@app.route('/get-latest-news', methods=['GET'])
def latest_news():
    """
    Gets the latest news
    """
    try:
        user = isUserAuthorized(request.headers.get('Authorization'))
        if not user:
            return ({ 'error': 'Please login again' }, http.client.UNAUTHORIZED)

        country = 'in'
        keyword = None
        if request.args:
            print(request.args)
            country = request.args.get('country')
            keyword = request.args.get('keyword')
        response = get_latest_news(apiKey=API_KEY, country=country, keyword=keyword)
        return jsonify([
            {
                "id": hash(news["url"]),
                "headline": news["title"],
                "shortDescription": news["description"],
                "url": news["url"],
                "image": news["urlToImage"],
                "date": news["publishedAt"]
            }
            for news in response["articles"]
        ])
    except Exception as e:
        return ({'error': f'Error occurred: {e}'}, http.client.INTERNAL_SERVER_ERROR)

@app.route('/saved-news', methods=['GET', 'POST'])
def saved_news():
    """
    Gets the saved news, Saves the given news.
    """
    try:
        user = isUserAuthorized(request.headers.get('Authorization'))
        if not user:
            return ({ 'error': 'Please login again' }, http.client.UNAUTHORIZED)

        if request.method == 'POST':
            news_obj = request.get_json()
            if SavedNews.query.get(news_obj['id']):
                return { "saved": True }
            else:
                news = SavedNews(id=news_obj['id'], headline=news_obj['headline'], url=news_obj['url'], image=news_obj['image'], shortDescription=news_obj['shortDescription'], date=parse(news_obj['date']), user_id=user.id)
                db.session.add(news)
                db.session.commit()
                return { "saved": True }
        else:
            all_news = SavedNews.query.filter_by(user_id=user.id)
            return jsonify([ news.serialize for news in all_news])
    except Exception as e:
        db.session.rollback()
        return ({'error': f'Error occurred: {e}'}, http.client.INTERNAL_SERVER_ERROR)

@app.route('/saved-news/<int(signed=True):id>', methods=['DELETE'])
def delete_saved_news(id):
    """
    Deletes the news from saved list by using the given id
    """
    try:
        user = isUserAuthorized(request.headers.get('Authorization'))
        if not user:
            return ({ 'error': 'Please login again' }, http.client.UNAUTHORIZED)

        news = SavedNews.query.get(id)
        if news:
            db.session.delete(news)
            db.session.commit()
            return { "deleted": True }
        return ({'error': 'Not found the saved news'}, http.client.NOT_FOUND)
    except Exception as e:
        db.session.rollback()
        return ({'error': f'Error occurred: {e}'}, http.client.INTERNAL_SERVER_ERROR)

@app.route('/countries')
def get_countries():
    """
    Countries available to fetch news.
    """
    user = isUserAuthorized(request.headers.get('Authorization'))
    if not user:
        return ({ 'error': 'Please login again' }, http.client.UNAUTHORIZED)

    return jsonify([
        'ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de', 'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 'lv', 'ma', 'mx', 'my', 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za'
    ])

@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    """
    Registers the user to the database.
    """
    try:
        user_credentials = request.get_json()
        password_hash = bcrypt.generate_password_hash(user_credentials['password'])
        user = User(username=user_credentials['username'], email=user_credentials['email'], password=password_hash.decode())
        db.session.add(user)
        db.session.commit()
        return { 'success': True }
    except Exception as e:
        db.session.rollback()
        return({ 'error': f'Error occurred: {e}'}, http.client.UNAUTHORIZED)

@app.route('/')
@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    """
    Returns the authorization token if user is already registered.
    """
    try:
        user_credentials = request.get_json()
        user = User.query.filter_by(username=user_credentials['username']).first()
        if user and bcrypt.check_password_hash(user.password, user_credentials['password']):
            auth_token = user.generateAuthToken()
            return jsonify(auth_token)
        else:
            return({'error': 'User credentials mismatch'}, http.client.UNAUTHORIZED)
    except Exception as e:
        return({ 'error': f'Error occurred: {e}'}, http.client.UNAUTHORIZED)

@app.route('/user-details', methods=['GET'])
def user_details():
    """
    Returns the details of the logged in user.
    """
    user = isUserAuthorized(request.headers.get('Authorization'))
    if not user:
        return ({ 'error': 'Please login again' }, http.client.UNAUTHORIZED)

    return jsonify(user.serialize)