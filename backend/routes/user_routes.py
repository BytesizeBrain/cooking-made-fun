import logging
import uuid
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from app import app, db
from models.user_model import User

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Declare this as a blueprint for user-related routes
users_bp = Blueprint('users', __name__)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Render the login page with a Google sign-in button
        return render_template('login.html') # TODO: Make page
    
    if request.method == 'POST':
        # Check if user is already logged in
        if 'username' in session:
            return redirect(url_for('main.index'))
        
        # Start OAuth flow by redirecting to Google's OAuth 2.0 server
        try:
            redirect_uri = url_for('authorize_google', _external=True)
            return google.authorize_redirect(redirect_uri)
        except Exception as e:
            logging.error(f"Error during Google OAuth redirect: {e}")
            return "An error occurred during login. Please try again.", 500


@users_bp.route('/authorize/google')
def authorize_google():
    try:
        # Get the token from Google
        token = google.authorize_access_token()
    except Exception as e:
        logging.error(f"Error during Google OAuth token exchange: {e}")
        return "An error occurred during login. Please try again.", 500

    try:
        # Get user information from google userinfo endpoint
        userinfo_endpoint = google.server_metadata['userinfo_endpoint']
        resp = google.get(userinfo_endpoint)
        user_info = resp.json()
    except Exception as e:
        logging.error(f"Error fetching user info from Google: {e}")
        return "An error occurred while fetching user information. Please try again.", 500

    # Check if user exists in DB, if not create new user
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        # Generate UUID for new user
        new_id = str(uuid.uuid4())
        user = User.query.filter_by(id=new_id).first()
        while user:
            logging.warning("UUID collision detected, generating a new UUID.")
            new_id = str(uuid.uuid4())
            user = User.query.filter_by(id=new_id).first()

        new_user = User(id=new_id, email=user_info['email'], display_name=user_info['name'])
        db.session.add(new_user)
        db.session.commit()
    
    # Log the user in (store info in session)
    session['oauth_token'] = token
    session['username'] = user_info['email']
    return redirect(url_for('main.index'))