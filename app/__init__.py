from flask import Flask
from flask_pymongo import PyMongo
from flask_smorest import Api
from flask_cors import CORS
import os

mongo = PyMongo()
api = Api()

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    
    # Chargement de la configuration
    app.config.from_object(config_class)
    
    # Configuration CORS
    frontend_url = os.getenv('FRONTEND_URL')
    CORS(app, resources={
        r"/api/*": {
            "origins": [frontend_url],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialisation des extensions
    mongo.init_app(app)
    api.init_app(app)
    
    # Enregistrement des blueprints
    from app.controllers.tesla_history_controller import bp as tesla_history_bp
    app.register_blueprint(tesla_history_bp)
    from app.controllers.graph_controller import graph_bp
    api.register_blueprint(graph_bp)
    from app.controllers.sales_controller import sales_bp
    api.register_blueprint(sales_bp)
    
    return app