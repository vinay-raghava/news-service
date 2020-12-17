import requests
import http.client

def get_latest_news(apiKey: str, country: str = None, keyword: str = None, category: str = None):
    """
    Gets the latest news from the news api.
    """
    if not apiKey:
        return ({"error": "API key not provided"}, http.client.UNAUTHORIZED)
    elif not (country or keyword or category):
        return ({"error": "No country or category or keyword specified"}, http.client.BAD_REQUEST)
    base_url = 'http://newsapi.org/v2/top-headlines'
    complete_url = base_url + '?' + 'apiKey=' + apiKey
    if country:
        complete_url = complete_url + '&country=' + country
    if keyword:
        complete_url = complete_url + '&q=' + keyword
    if category:
        complete_url = complete_url + '&category=' + category

    return requests.get(complete_url).json()