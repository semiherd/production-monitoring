from flask import Blueprint, request, jsonify, send_file
from app.services.tasks import generate_export_task
from rbac import require_roles
import os
bp = Blueprint("export", __name__)
@bp.post("/<report_slug>")
@require_roles("admin","manager","engineer","operator")
def start_export(report_slug):
    fmt = (request.args.get("format") or "pdf").lower()
    task = generate_export_task.delay(report_slug, fmt)
    return jsonify({"task_id": task.id, "status": "queued"}), 202
@bp.get("/status/<task_id>")
def check_status(task_id):
    from app import celery
    task = celery.AsyncResult(task_id)
    if task.state == "SUCCESS":
        return jsonify({"status": "completed", "result": task.result})
    elif task.state == "FAILURE":
        return jsonify({"status": "failed", "error": str(task.info)}), 500
    else:
        return jsonify({"status": task.state}), 200
@bp.get("/download/<filename>")
@require_roles("admin","manager","engineer","operator")
def download(filename):
    path = os.path.join(os.getenv("EXPORT_DIR", "/tmp/exports"), filename)
    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404
    ext = filename.split(".")[-1].lower()
    mimetype = "application/octet-stream"
    if ext == "pdf": mimetype = "application/pdf"
    elif ext == "csv": mimetype = "text/csv"
    elif ext == "xlsx": mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return send_file(path, as_attachment=True, download_name=filename, mimetype=mimetype)
