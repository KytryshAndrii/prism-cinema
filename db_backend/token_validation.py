from functools import wraps
from flask import request, jsonify
import os
import jwt

JWT_SECRET = os.getenv("JWT_SECRET_KEY", "fallback_secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return jsonify({"message": "Token missing"}), 401
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            request.user = data  # możesz użyć dalej
        except:
            return jsonify({"message": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated
