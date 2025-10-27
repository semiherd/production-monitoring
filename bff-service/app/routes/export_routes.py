from flask import Blueprint, request, jsonify, current_app, Response, make_response
from ..services.http import post, get
from ..middleware.auth_middleware import require_roles

bp = Blueprint("bff_export", __name__)
def _auth_header(token): return {"Authorization": f"Bearer {token}"} if token else {}

@bp.post("/<report_slug>")
@require_roles("admin","manager","engineer","operator")
def start_export(report_slug):
    token = request.cookies.get(current_app.config["ACCESS_COOKIE_NAME"])
    r = post(current_app.config["EXPORT_BASE_URL"], f"/api/export/{report_slug}", headers=_auth_header(token), json=None)
    return (r.content, r.status_code, r.headers.items())

@bp.get("/status/<task_id>")
def status(task_id):
    r = get(current_app.config["EXPORT_BASE_URL"], f"/api/export/status/{task_id}")
    return (r.content, r.status_code, r.headers.items())

@bp.get("/download/<filename>")
@require_roles("admin","manager","engineer","operator")
def download(filename):
    token = request.cookies.get(current_app.config["ACCESS_COOKIE_NAME"])
    r = get(current_app.config["EXPORT_BASE_URL"], f"/api/export/download/{filename}", headers=_auth_header(token), stream=True)
    resp = Response(r.iter_content(chunk_size=8192), status=r.status_code)
    for k,v in r.headers.items():
        if k.lower().startswith(("content-", "content-disposition")): resp.headers[k]=v
    return resp
