import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session

users_bp = Blueprint('users', __name__)

@users_bp.route('/login', methods=['POST'])
def login():
    # Check if user is already logged in
    # Google OAuth login
    # Get user info from Google and write to DB if new user
    pass


@users_bp.route('/api/users/register', methods=['POST'])
def register():
    # Print logger message for debugging
    logging.info("Register endpoint called")
    data = request.get_json()

    full_name = data.get('full_name')
    email = data.get('email')
    password_hash = data.get('password_hash')

    if not full_name or not email or not password_hash:
        return jsonify({"error": "Missing required fields"}), 400
    
    from app.models import User, db
    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    # Create and add new user
    new_user = User(full_name=full_name, email=email, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"{email} Registered"}), 201
