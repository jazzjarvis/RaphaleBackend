from flask import Blueprint, request, jsonify
from app.models import User

from app.utils.jwt_handler import encode_auth_token
from app.extensions import db,bcrypt




auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"message": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    token = encode_auth_token(new_user.id)
    return jsonify({
        "username": new_user.username,
        "email": new_user.email,
        "id": new_user.id,
        "token": token
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email_or_username = data.get('username')  
    password = data.get('password')

    user = User.query.filter((User.username == email_or_username) | (User.email == email_or_username)).first()

    if user and bcrypt.check_password_hash(user.password, password):
        token = encode_auth_token(user.id)
        return jsonify({
            "username": user.username,
            "email": user.email,
            "id": user.id,
            "token": token
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401
