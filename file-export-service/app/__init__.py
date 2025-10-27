from flask import Flask
from flask_cors import CORS
from celery import Celery
from .config import Config, init_celery

celery = Celery(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, origins="*")
    from .routes.export_routes import bp as export_bp
    app.register_blueprint(export_bp, url_prefix="/api/export")
    init_celery(celery, app)
    return app
