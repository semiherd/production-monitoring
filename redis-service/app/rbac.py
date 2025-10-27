import time, requests, jwt, base64
from functools import wraps
from flask import request, jsonify
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.primitives import serialization
from .config import Config

_JWKS_CACHE = {"exp": 0, "keys": {}}

def _get_jwks():
    if _JWKS_CACHE["exp"] > time.time():
        return _JWKS_CACHE["keys"]
    resp = requests.get(Config.AUTH_JWKS_URL, timeout=5)
    resp.raise_for_status()
    keys = {k["kid"]: k for k in resp.json().get("keys", [])}
    _JWKS_CACHE["keys"] = keys
    _JWKS_CACHE["exp"] = time.time() + 600
    return keys

def _public_key_from_jwk(jwk):
    def b64u_int(s): return int.from_bytes(base64.urlsafe_b64decode(s + "=="), "big")
    pub = RSAPublicNumbers(b64u_int(jwk["e"]), b64u_int(jwk["n"])).public_key()
    return pub.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

def require_roles(*roles):
    def decorator(f):
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization", "").replace("Bearer ", "")
            if not token:
                return jsonify({"error":"missing token"}), 401
            try:
                unverified = jwt.get_unverified_header(token)
                kid = unverified.get("kid")
                jwks = _get_jwks()
                jwk = jwks.get(kid)
                if not jwk:
                    return jsonify({"error":"unknown kid"}), 401
                pub_pem = _public_key_from_jwk(jwk)
                claims = jwt.decode(token, pub_pem, algorithms=["RS256"], audience=Config.JWT_AUDIENCE, issuer=Config.JWT_ISSUER)
            except Exception as e:
                return jsonify({"error":"invalid token", "detail": str(e)}), 401
            if roles and claims.get("role") not in roles:
                return jsonify({"error":"forbidden", "role": claims.get("role")}), 403
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator
