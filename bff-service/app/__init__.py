from flask import Flask
from flask_cors import CORS
from .config import Config
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    if Config.CORS_ALLOW_ORIGIN:
        CORS(app, resources={r"/api/*": {"origins": [Config.CORS_ALLOW_ORIGIN]}}, supports_credentials=True)
    from .routes.auth_routes import bp as auth_bp
    from .routes.export_routes import bp as export_bp
    from .routes.redis_routes import bp as redis_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(export_bp, url_prefix="/api/export")
    app.register_blueprint(redis_bp, url_prefix="/api/redis")
    @app.get("/api/healthz")
    def healthz(): return {"ok": True}
    return app
