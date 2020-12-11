import http.client
import uuid
import os
from dateutil.parser import parse
from flask import request, jsonify, url_for, send_file
from flask_cors import cross_origin
from news_app import app, db, config
from news_app.models import SavedNews
from news_app.utils.convert_to_json import convert_to_json
from news_app.utils.latest_news_getter import get_latest_news

API_KEY = config.NEWS_API_KEY

@app.route('/')
@app.route('/get-latest-news', methods=['GET'])
@cross_origin()
def latest_news():
    """
    Gets the latest news
    """

    response = get_latest_news(apiKey=API_KEY, country='in')
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


@app.route('/saved-news', methods=['GET', 'POST'])
@cross_origin()
def saved_news():
    """
    Gets the saved news, Saves the given news.
    """
    if request.method == 'POST':
         news_obj = request.get_json()
         if SavedNews.query.get(news_obj['id']):
             return ({"error": 'Integrity error'}, http.client.INTERNAL_SERVER_ERROR)
         else:
             news = SavedNews(id=news_obj['id'], headline=news_obj['headline'], url=news_obj['url'], image=news_obj['image'], shortDescription=news_obj['shortDescription'], date=parse(news_obj['date']))
             db.session.add(news)
             db.session.commit()
             return { "saved": True }

    else:
        all_news = SavedNews.query.all()
        for news in all_news:
            news.saved = True
        return convert_to_json.getNews(all_news)

@app.route('/saved-news/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_saved_news(id):
    """
    Deletes the news from saved list by using the given id
    """
    news = SavedNews.query.get(id)
    if news:
        db.session.delete(news)
        db.session.commit()
        return { "deleted": True }
    return ({"error": 'Not found the saved news'}, http.client.NOT_FOUND)

@app.route('/countries')
@cross_origin()
def get_countries():
    """
    Countries available to fetch news.
    """
    return jsonify([
        'ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de', 'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 'lv', 'ma', 'mx', 'my', 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za'
    ])