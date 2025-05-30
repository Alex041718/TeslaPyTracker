import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-very-secret'
    MONGO_URI = 'mongodb://flasktesla:alexPass@mongodb:27017/flaskapp'
    DEBUG = True