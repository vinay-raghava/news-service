import http.client
from flask import Blueprint, request, jsonify, current_app
from dateutil.parser import parse
from news_app.utils.check_authorization import isUserAuthorized
from news_app.news.utils import get_latest_news
from news_app import db
from news_app.models import SavedNews

news = Blueprint('news', __name__)

@news.route('/get-latest-news', methods=['GET'])
def latest_news():
    db.drop_all()
    db.create_all() # will remove once the new tables are created with many to many association
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
            country = request.args.get('country')
            keyword = request.args.get('keyword')
        response = get_latest_news(apiKey=current_app.config['NEWS_API_KEY'], country=country, keyword=keyword)
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

@news.route('/saved-news', methods=['GET', 'POST'])
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
            saved_news = SavedNews.query.get(news_obj['id'])
            if saved_news:
                if user in saved_news.users:
                    return {"saved": True}
                else:
                    saved_news.users.append(user)
                    db.session.add(saved_news)
                    db.session.commit()
                    return { "saved": True }
            else:
                news = SavedNews(id=news_obj['id'], headline=news_obj['headline'], url=news_obj['url'], image=news_obj['image'], shortDescription=news_obj['shortDescription'], date=parse(news_obj['date']), users=[user])
                db.session.add(news)
                db.session.commit()
                return { "saved": True }
        else:
            all_news = user.savedNews
            return jsonify([ news.serialize for news in all_news])
    except Exception as e:
        db.session.rollback()
        return ({'error': f'Error occurred: {e}'}, http.client.INTERNAL_SERVER_ERROR)

@news.route('/saved-news/<int(signed=True):id>', methods=['DELETE'])
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
            user.savedNews.remove(news)
            if not len(news.users):
                db.session.delete(news)
            db.session.commit()
            return { "deleted": True }
        return ({'error': 'Not found the saved news'}, http.client.NOT_FOUND)
    except Exception as e:
        db.session.rollback()
        return ({'error': f'Error occurred: {e}'}, http.client.INTERNAL_SERVER_ERROR)

@news.route('/countries')
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