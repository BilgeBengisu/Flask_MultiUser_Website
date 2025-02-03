import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_random_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # SQLite for simplicity, you can use PostgreSQL or MySQL in production
