from flask import Flask
from app.extensions import db, bcrypt
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Register blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app