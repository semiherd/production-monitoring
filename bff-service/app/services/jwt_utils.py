import time, requests, jwt, base64
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.primitives import serialization
from flask import current_app
_JWKS_CACHE = {"exp": 0, "keys": {}}
def _get_jwks():
    if _JWKS_CACHE["exp"] > time.time():
        return _JWKS_CACHE["keys"]
    resp = requests.get(current_app.config["AUTH_JWKS_URL"], timeout=5); resp.raise_for_status()
    keys = {k["kid"]: k for k in resp.json().get("keys", [])}
    _JWKS_CACHE["keys"] = keys; _JWKS_CACHE["exp"] = time.time() + 600; return keys
def _public_key_from_jwk(jwk):
    def b64u_int(s): return int.from_bytes(base64.urlsafe_b64decode(s + "=="), "big")
    pub = RSAPublicNumbers(b64u_int(jwk["e"]), b64u_int(jwk["n"])).public_key()
    return pub.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
def decode_access(token: str):
    unverified = jwt.get_unverified_header(token); kid = unverified.get("kid")
    jwks = _get_jwks(); jwk = jwks.get(kid)
    if not jwk: raise ValueError("unknown kid")
    pub_pem = _public_key_from_jwk(jwk)
    return jwt.decode(token, pub_pem, algorithms=["RS256"], audience=current_app.config["JWT_AUDIENCE"], issuer=current_app.config["JWT_ISSUER"])
