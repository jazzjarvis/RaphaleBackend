from flask import Blueprint, request, jsonify
from app.extensions import db, bcrypt
from app.utils.jwt_handler import encode_auth_token
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    token = encode_auth_token(new_user.id)
    return jsonify({
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    identifier = data.get('username')  # Can be username or email
    password = data.get('password')

    if not identifier or not password:
        return jsonify({"error": "Missing credentials"}), 400

    user = User.query.filter(
        (User.username == identifier) | 
        (User.email == identifier)
    ).first()

    if user and bcrypt.check_password_hash(user.password, password):
        token = encode_auth_token(user)
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "token": token
            }
        }), 200

    return jsonify({"error": "Invalid credentials"}), 401