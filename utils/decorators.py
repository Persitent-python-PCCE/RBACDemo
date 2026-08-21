from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt
from flask import request, jsonify, render_template


def role_required(*roles):#allowed roles
    def decorator(function):
        @wraps(function)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") not in roles:
                if request.is_json or request.path.startswith("/api"):
                    return jsonify({
                        "message": "Forbidden"
                    }), 403
                return render_template("403.html", error="Forbidden: You do not have permission to access this page"), 403

            return function(*args, **kwargs)
        return wrapper
    return decorator
