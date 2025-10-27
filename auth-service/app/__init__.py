from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app, origins="*")

    from .routes.auth_routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    return app
