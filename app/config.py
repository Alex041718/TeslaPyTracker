import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-very-secret'
    MONGO_URI = 'mongodb://flasktesla:alexPass@mongodb:27017/flaskapp'
    DEBUG = True
    
    # Configuration Flask-Smorest
    API_TITLE = 'Tesla Tracker API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/api/docs'
    OPENAPI_SWAGGER_UI_PATH = '/swagger'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'