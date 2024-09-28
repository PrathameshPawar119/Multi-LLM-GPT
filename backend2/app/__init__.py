from flask import Flask
from flask_cors import CORS
from app.utils.json_encoder import JSONEncoder
from app.utils.dbconnect import dbconnect
from app.routes import auth_routes, chat_routes, user_routes

def create_app():
    app = Flask(__name__)
    app.json_encoder = JSONEncoder
    CORS(app)

    db = dbconnect()

    # Register blueprints
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(chat_routes.bp)
    app.register_blueprint(user_routes.bp)

    return app
