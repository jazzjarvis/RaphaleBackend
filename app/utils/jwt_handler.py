import jwt
import datetime
import jwt
from datetime import datetime, timedelta
from flask import current_app

def encode_auth_token(user):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': user.id,
            'username': user.username,
            'email': user.email
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    except Exception as e:
        current_app.logger.error(f"JWT encoding failed: {str(e)}")
        return None
def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'
