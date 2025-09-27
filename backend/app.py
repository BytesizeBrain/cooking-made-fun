from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from .routes.user_routes import users_bp
import os
from dotenv import load_dotenv

if __name__ in '__main__':

    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()
    app.secret_key = os.getenv('SECRET_KEY')
    if not app.secret_key:
        raise ValueError("No SECRET_KEY set for Flask application. Did you forget to set it in the .env file?")

    # Configuring SQLAlchemy ORM to use database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Only used for event signals (which are not used in our project)
    db = SQLAlchemy(app)

    # Registering Blueprints (Routes)
    app.register_blueprint(users_bp)


    # Create a db and tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)