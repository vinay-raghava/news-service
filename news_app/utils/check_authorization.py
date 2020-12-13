from news_app.models import User

def isUserAuthorized(auth_header):
    """
    Checks the user authorization
    """
    auth_token = auth_header
    if not auth_token:
        return None
    user_id = User.decodeAuthToken(auth_token)
    user = User.query.filter_by(id=user_id).first()
    return user