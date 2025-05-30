import os

class Config:
    SECRET_KEY = 'your-secret-key'  # Use env var in production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
