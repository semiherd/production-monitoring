from flask import Blueprint, request, current_app
from ..services.http import get, post
from ..middleware.auth_middleware import require_roles
bp = Blueprint("bff_redis", __name__)
def _auth_header(token): return {"Authorization": f"Bearer {token}"} if token else {}
@bp.get("/health")
@require_roles("admin","manager","engineer","operator")
def health():
    token = request.cookies.get(current_app.config["ACCESS_COOKIE_NAME"])
    r = get(current_app.config["REDIS_BASE_URL"], "/api/health", headers=_auth_header(token))
    return (r.content, r.status_code, r.headers.items())
@bp.get("/info")
@require_roles("admin","engineer","manager")
def info():
    token = request.cookies.get(current_app.config["ACCESS_COOKIE_NAME"])
    r = get(current_app.config["REDIS_BASE_URL"], "/api/info", headers=_auth_header(token))
    return (r.content, r.status_code, r.headers.items())
