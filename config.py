import os

class Config:
    SECRET_KEY = 'supersecretkey'
    # Use SQLite database file stored locally in the project folder
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lms.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
