from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    
    # Chargement de la configuration
    app.config.from_object(config_class)
    
    # Initialisation de MongoDB
    mongo.init_app(app)
    
    # Enregistrement des blueprints
    from app.controllers.user_controller import user_bp
    app.register_blueprint(user_bp)
    from app.controllers.tesla_history_controller import bp as tesla_history_bp
    app.register_blueprint(tesla_history_bp)
    
    return app