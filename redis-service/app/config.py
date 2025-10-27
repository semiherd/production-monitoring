import os
class Config:
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
    AUTH_JWKS_URL = os.getenv("AUTH_JWKS_URL", "http://auth-service:5001/.well-known/jwks.json")
    JWT_ISSUER = os.getenv("JWT_ISSUER", "https://auth.service.local")
    JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "smartline")
