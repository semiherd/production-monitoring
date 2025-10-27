import os, hashlib, base64

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg2://smartline:smartline@postgres:5432/smartline_auth")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS   = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    JWT_PRIVATE_KEY_PEM = os.getenv("JWT_PRIVATE_KEY_PEM")
    JWT_PUBLIC_KEY_PEM  = os.getenv("JWT_PUBLIC_KEY_PEM")
    JWT_ISSUER   = os.getenv("JWT_ISSUER", "https://auth.service.local")
    JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "smartline")
    SECRET_KEY   = os.getenv("JWT_SECRET_FALLBACK", "fallback-secret")

def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def jwk_from_public_pem(public_pem: str):
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    key = serialization.load_pem_public_key(public_pem.encode("utf-8"))
    if not isinstance(key, rsa.RSAPublicKey):
        raise ValueError("Public key is not RSA")
    nums = key.public_numbers()
    n = _b64url(nums.n.to_bytes((nums.n.bit_length() + 7)//8, "big"))
    e = _b64url(nums.e.to_bytes((nums.e.bit_length() + 7)//8, "big"))
    kid = hashlib.sha256((n + "." + e).encode()).hexdigest()[:16]
    return {"kty": "RSA", "use": "sig", "alg": "RS256", "kid": kid, "n": n, "e": e}
