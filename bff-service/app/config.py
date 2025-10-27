import os
class Config:
    AUTH_BASE_URL   = os.getenv("AUTH_BASE_URL",   "http://auth-service:5001")
    EXPORT_BASE_URL = os.getenv("EXPORT_BASE_URL", "http://export-service:5002")
    REDIS_BASE_URL  = os.getenv("REDIS_BASE_URL",  "http://redis-service:5003")
    SECRET_KEY = os.getenv("BFF_SECRET_KEY", "dev-only-secret")
    ACCESS_COOKIE_NAME = os.getenv("ACCESS_COOKIE_NAME", "access_token")
    REFRESH_COOKIE_NAME = os.getenv("REFRESH_COOKIE_NAME", "refresh_token")
    COOKIE_SECURE = os.getenv("COOKIE_SECURE", "true").lower() == "true"
    COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "Lax")
    COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN", None)
    CORS_ALLOW_ORIGIN = os.getenv("CORS_ALLOW_ORIGIN", "http://localhost:3000")
    CERT_DIR = os.getenv("CERT_DIR", "/certs")
    CERT_FILE = os.getenv("CERT_FILE", f"{CERT_DIR}/server.crt")
    KEY_FILE  = os.getenv("KEY_FILE",  f"{CERT_DIR}/server.key")
    AUTH_JWKS_URL = os.getenv("AUTH_JWKS_URL", "http://auth-service:5001/.well-known/jwks.json")
    JWT_ISSUER = os.getenv("JWT_ISSUER", "https://auth.service.local")
    JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "smartline")
