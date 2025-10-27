from flask import Blueprint, jsonify, request
from .redis_client import r
from .rbac import require_roles

bp = Blueprint("redis_api", __name__)

@bp.get("/api/health")
@require_roles("admin","engineer","manager","operator")
def health():
    try:
        return jsonify({"status":"ok","ping": r.ping()})
    except Exception as e:
        return jsonify({"status":"error","detail":str(e)}), 500

@bp.get("/api/info")
@require_roles("admin","engineer","manager")
def info():
    info = r.info()
    keys = {k: info.get(k) for k in ["connected_clients","used_memory_human","total_commands_processed","uptime_in_seconds"]}
    return jsonify(keys)

@bp.get("/api/keys")
@require_roles("admin","engineer")
def keys():
    pattern = request.args.get("pattern","*")
    return jsonify({"keys": r.keys(pattern)})

@bp.post("/api/flush")
@require_roles("admin")
def flush():
    r.flushdb(); return jsonify({"message":"Database cleared"})

@bp.get("/api/get/<key>")
@require_roles("admin","engineer","manager","operator")
def get_key(key):
    return jsonify({"key": key, "value": r.get(key)})

@bp.post("/api/set/<key>")
@require_roles("admin","engineer")
def set_key(key):
    data = request.get_json() or {}
    if "value" not in data: return jsonify({"error":"missing value"}), 400
    r.set(key, data["value"]); return jsonify({"key": key, "value": data["value"], "status":"ok"})
