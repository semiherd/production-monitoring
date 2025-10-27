import os
class Config:
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret")
    CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://redis-service:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://redis-service:6379/0")
    AUTH_JWKS_URL = os.getenv("AUTH_JWKS_URL", "http://auth-service:5001/.well-known/jwks.json")
    JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "smartline")
    JWT_ISSUER = os.getenv("JWT_ISSUER", "https://auth.service.local")

def init_celery(celery, app):
    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
