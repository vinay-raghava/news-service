from flask import jsonify
from news_app.models import SavedNews

class convert_to_json():
    """
    Converts the given data to json
    """
    def getNews(saved_news: [SavedNews]):
        """
        Converts the SavedNews data model to json
        """
        news = [{
            "id": news.id,
            "headline": news.headline,
            "url": news.url,
            "image": news.image,
            "shortDescription": news.shortDescription,
            "saved": True,
            "date": news.date,
            "savedDate": news.savedDate
        } for news in saved_news ]
        return jsonify(news)