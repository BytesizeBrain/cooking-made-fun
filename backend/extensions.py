from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

app.config['FRONTEND_URL'] = os.getenv('FRONTEND_URL', 'http://localhost:5173/')

app.config['JWT_SECRET'] = os.getenv('SECRET_KEY')
if not app.config['JWT_SECRET']:
    raise ValueError("No SECRET_KEY set for Flask application. Did you forget to set it in the .env file?")

google_client_id = os.getenv('CLIENT_ID')
google_client_secret = os.getenv('CLIENT_SECRET')
if not google_client_id or not google_client_secret:
    raise ValueError("No CLIENT_ID or CLIENT_SECRET set for Google OAuth. Did you forget to set it in the .env file?")
app.config['GOOGLE_CLIENT_ID'] = google_client_id
app.config['GOOGLE_CLIENT_SECRET'] = google_client_secret

# Configuring SQLAlchemy ORM to use database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)