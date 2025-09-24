import logging
from flask import Blueprint, request, jsonify

users_bp = Blueprint('users', __name__)

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
    
    # Write user information to database
    # Either by creating an ORM object or writing raw SQL

    return jsonify({"message": f"{email} Registered"}), 201