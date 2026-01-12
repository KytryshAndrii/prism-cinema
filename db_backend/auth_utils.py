import jwt
import datetime
import os

JWT_SECRET = os.getenv("JWT_SECRET_KEY", "fallback_secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def generate_token(user_id: str, expires_in=21600):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload["user_id"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
