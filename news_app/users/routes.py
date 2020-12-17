import http.client
from flask_cors import cross_origin
from flask import Blueprint, request, jsonify
from news_app.utils.check_authorization import isUserAuthorized
from news_app import bcrypt, db
from news_app.models import User

users = Blueprint('users', __name__)

@users.route('/register', methods=['POST'])
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

@users.route('/')
@users.route('/login', methods=['POST'])
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

@users.route('/user-details', methods=['GET'])
def user_details():
    """
    Returns the details of the logged in user.
    """
    user = isUserAuthorized(request.headers.get('Authorization'))
    if not user:
        return ({ 'error': 'Please login again' }, http.client.UNAUTHORIZED)

    return jsonify(user.serialize)