import jwt, datetime, uuid
from flask import current_app

ALG = "RS256"

def _keys():
    return current_app.config.get("JWT_PRIVATE_KEY_PEM"), current_app.config.get("JWT_PUBLIC_KEY_PEM")

def _kid(public_pem: str) -> str:
    from app.config import jwk_from_public_pem
    return jwk_from_public_pem(public_pem)["kid"]

def create_access_token(username: str, role: str) -> str:
    priv, pub = _keys()
    now = datetime.datetime.utcnow()
    payload = {
        "iss": current_app.config["JWT_ISSUER"],
        "aud": current_app.config["JWT_AUDIENCE"],
        "sub": username,
        "role": role,
        "type": "access",
        "iat": now,
        "exp": now + datetime.timedelta(minutes=current_app.config["ACCESS_TOKEN_EXPIRE_MINUTES"]),
        "jti": uuid.uuid4().hex,
    }
    headers = {"alg": ALG, "typ": "JWT"}
    if pub: headers["kid"] = _kid(pub)
    if priv: return jwt.encode(payload, priv, algorithm=ALG, headers=headers)
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256", headers=headers)
