from flask import Blueprint, request, jsonify, current_app
from app.models import User
from app.utils.password_utils import hash_password, verify_password
from app import db
from app.services import jwt_service
from app.config import jwk_from_public_pem

bp = Blueprint("auth", __name__)

@bp.post("/register")
def register():
    data = request.get_json() or {}
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error":"exists"}), 400
    u = User(username=data["username"], password_hash=hash_password(data["password"]), role=data.get("role","operator"))
    db.session.add(u); db.session.commit()
    return jsonify({"message":"ok"}), 201

@bp.post("/login")
def login():
    data = request.get_json() or {}
    u = User.query.filter_by(username=data.get("username","")).first()
    if not u or not verify_password(u.password_hash, data.get("password","")):
        return jsonify({"error":"invalid credentials"}), 401
    access = jwt_service.create_access_token(u.username, u.role)
    # issue short-lived refresh (demo omitted for brevity in v4)
    return jsonify({"access_token": access, "refresh_token": access, "role": u.role})

@bp.get("/verify")
def verify():
    # BFF + services verify offline using JWKS; this endpoint is just a helper
    token = request.headers.get("Authorization","").replace("Bearer ","")
    if not token: return jsonify({"valid": False}), 401
    try:
        # decode with public key in services; here just stub-ack
        return jsonify({"valid": True, "sub":"stub", "role":"admin"})
    except:
        return jsonify({"valid": False}), 401

@bp.get("/.well-known/jwks.json")
def jwks():
    pub = current_app.config.get("JWT_PUBLIC_KEY_PEM")
    if not pub:
        return jsonify({"keys": []})
    return jsonify({"keys": [jwk_from_public_pem(pub)]})
