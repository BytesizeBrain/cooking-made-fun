import logging
import uuid
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from extensions import app, db
from models.user_model import User

# Configure logging to see debug messages
logging.basicConfig(level=logging.DEBUG)

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
        return render_template('login.html')
    
    if request.method == 'POST':
        logging.debug("POST request received for login")
        
        # Check if user is already logged in
        if 'email' in session:
            logging.debug("User already logged in, redirecting to index")
            return redirect(url_for('main.index'))
        
        # Start OAuth flow by redirecting to Google's OAuth 2.0 server
        try:
            redirect_uri = url_for('users.authorize_google', _external=True)
            logging.debug(f"Redirect URI: {redirect_uri}")
            logging.debug("About to call google.authorize_redirect")
            return google.authorize_redirect(redirect_uri)
        except Exception as e:
            logging.error(f"Error during Google OAuth redirect: {e}")
            import traceback
            logging.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({"error": "An error occurred during login. Please try again."}), 500

@users_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('users.login'))

@users_bp.route('/authorize/google')
def authorize_google():
    try:
        # Get the token from Google
        token = google.authorize_access_token()
    except Exception as e:
        logging.error(f"Error during Google OAuth token exchange: {e}")
        return jsonify({"error": "An error occurred during login. Please try again."}), 500

    try:
        # Get user information from google userinfo endpoint
        userinfo_endpoint = google.server_metadata['userinfo_endpoint']
        resp = google.get(userinfo_endpoint)
        user_info = resp.json()
    except Exception as e:
        logging.error(f"Error fetching user info from Google: {e}")
        return jsonify({"error": "An error occurred while fetching user information. Please try again."}), 500
    
    session['oauth_token'] = token
    session['email'] = user_info['email']

    # Check if user exists in DB, if not create new user
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        session['display_name'] = user_info['name']
        session['profile_pic'] = user_info.get('picture', "https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg")
        return redirect(url_for('users.complete_profile'))
    
    # Return the user to the index page
    return redirect(url_for('main.index'))

@users_bp.route('/profile/complete', methods=['GET', 'POST'])
def complete_profile():
    if 'email' not in session:
        return redirect(url_for('users.login'))
    
    if request.method == 'GET':
        # TODO: Make this page
        return render_template('complete_profile.html', email=session['email'], display_name=session.get('display_name', ''), profile_pic=session.get('profile_pic', 'https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg'))
    
    if request.method == 'POST':
        display_name = request.form.get('display_name')
        username = request.form.get('username')
        profile_pic = request.form.get('profile_pic', "https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg")
        
        if not display_name or not username:
            return jsonify({"error": "Display name and username are required."}), 400  # UI should prevent this, this is just a fallback
        
        # Check if username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"error": "Username already taken. Please choose another one."}), 400  # Ideally, the UI calls the GET /api/user/check_username with the username beforehand to avoid this, this is just a fallback
        
        # Generate UUID for new user
        new_id = str(uuid.uuid4())
        user = User.query.filter_by(id=new_id).first()
        while user:
            logging.warning("UUID collision detected, generating a new UUID.")
            new_id = str(uuid.uuid4())
            user = User.query.filter_by(id=new_id).first()

        new_user = User(id=new_id, email=session['email'], display_name=display_name, username=username, profile_pic=profile_pic)
        db.session.add(new_user)
        db.session.commit()
        
        # Clear session variables used during profile completion
        session.pop('display_name', None)
        session.pop('profile_pic', None)
        
        return redirect(url_for('main.index'))

# Pure API Routes (No page rendering)

@users_bp.route('/api/user/update', methods=['PUT'])
def update_user():
    if 'email' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user = User.query.filter_by(email=session['email']).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.json
    updated = False

    if 'display_name' in data and data['display_name'] is not None:
        user.display_name = data['display_name']
        updated = True
    if 'profile_pic' in data and data['profile_pic'] is not None:
        user.profile_pic = data['profile_pic']
        updated = True
    if 'username' in data and data['username'] is not None and not User.query.filter_by(username=data['username']).first():
        user.username = data['username']
        updated = True
    
    if updated:
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"message": "No valid fields to update"}), 400

# API to be used during registration and name changes to check if a username is already taken
@users_bp.route('/api/user/check_username', methods=['GET'])
def check_username():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({"error": "Username parameter is required"}), 400
    
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"exists": True}), 200
    else:
        return jsonify({"exists": False}), 200