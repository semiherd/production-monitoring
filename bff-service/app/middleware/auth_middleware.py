from functools import wraps
from flask import request, jsonify
from ..services.jwt_utils import decode_access

def require_roles(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.cookies.get("access_token") or request.headers.get("Authorization","").replace("Bearer ","")
            if not token: return jsonify({"error":"missing token"}), 401
            try: claims = decode_access(token)
            except Exception as e: return jsonify({"error":"invalid token","detail":str(e)}), 401
            if roles and claims.get("role") not in roles: return jsonify({"error":"forbidden","role":claims.get("role")}), 403
            request.user = claims; return f(*args, **kwargs)
        return wrapper
    return decorator
