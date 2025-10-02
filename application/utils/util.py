from datetime import datetime, timedelta, timezone
from jose import jwt
import jose
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "a super secret, secret key"  # production'da env değişkeni yap

def encode_token(user_id):
    """Kullanıcı ID üzerinden JWT üretir"""
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),  # 1 saat geçerli
        "iat": datetime.now(timezone.utc),  # issued at
        "sub": str(user_id)  # subject = user_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def token_required(f):
    """Token doğrulama decorator"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            try:
                token = request.headers["Authorization"].split(" ")[1]
            except IndexError:
                return jsonify({"message": "Token formatı yanlış!"}), 401

        if not token:
            return jsonify({"message": "Token eksik!"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = data["sub"]
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({"message": "Token süresi doldu!"}), 401
        except jose.exceptions.JWTError:
            return jsonify({"message": "Token geçersiz!"}), 401

        return f(user_id, *args, **kwargs)

    return decorated
