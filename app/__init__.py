from flask import Flask
from flask_pymongo import PyMongo
from flask_smorest import Api

mongo = PyMongo()
api = Api()

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    
    # Chargement de la configuration
    app.config.from_object(config_class)
    
    # Initialisation des extensions
    mongo.init_app(app)
    api.init_app(app)
    
    # Enregistrement des blueprints
    from app.controllers.user_controller import user_bp
    app.register_blueprint(user_bp)
    from app.controllers.tesla_history_controller import bp as tesla_history_bp
    app.register_blueprint(tesla_history_bp)
    from app.controllers.graph_controller import graph_bp
    api.register_blueprint(graph_bp)
    
    return app