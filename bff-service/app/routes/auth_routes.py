from flask import Blueprint, request, jsonify, current_app, make_response
from ..services.http import post, get
bp = Blueprint("bff_auth", __name__)

def _cookie_opts():
    return {"secure": current_app.config["COOKIE_SECURE"], "samesite": current_app.config["COOKIE_SAMESITE"], "domain": current_app.config["COOKIE_DOMAIN"], "httponly": True, "path": "/", "max_age": None}

@bp.post("/login")
def login():
    data = request.get_json() or {}
    r = post(current_app.config["AUTH_BASE_URL"], "/api/auth/login", json=data)
    if r.status_code != 200: return (r.text, r.status_code, r.headers.items())
    body = r.json(); access = body.get("access_token"); refresh = body.get("refresh_token"); role = body.get("role")
    resp = make_response({"ok": True, "role": role}); opts = _cookie_opts()
    resp.set_cookie(current_app.config["ACCESS_COOKIE_NAME"], access, **opts)
    resp.set_cookie(current_app.config["REFRESH_COOKIE_NAME"], refresh, **opts); return resp

@bp.post("/logout")
def logout():
    resp = make_response({"ok": True}); opts = _cookie_opts()
    resp.delete_cookie(current_app.config["ACCESS_COOKIE_NAME"], path="/", domain=opts["domain"])
    resp.delete_cookie(current_app.config["REFRESH_COOKIE_NAME"], path="/", domain=opts["domain"]); return resp

@bp.get("/me")
def me():
    token = request.cookies.get(current_app.config["ACCESS_COOKIE_NAME"])
    if not token: return jsonify({"authenticated": False}), 200
    r = get(current_app.config["AUTH_BASE_URL"], "/api/auth/verify", headers={"Authorization": f"Bearer {token}"})
    if r.status_code == 200: j = r.json(); return jsonify({"authenticated": True, "user": {"sub": j.get("sub"), "role": j.get("role")}})
    return jsonify({"authenticated": False}), 200
