from flask import request, jsonify
from marshmallow import ValidationError
from application.extensions import db, limiter, cache
from application.models import Member
from . import members_bp
from .schemas import member_schema, members_schema
from application.utils.util import encode_token, token_required
from werkzeug.security import generate_password_hash, check_password_hash

# GET ALL MEMBERS (with pagination)
@members_bp.get("")
@cache.cached(timeout=60)
def list_members():
    limit = request.args.get("limit", type=int, default=10)
    offset = request.args.get("offset", type=int, default=0)

    query = Member.query.order_by(Member.id.desc())
    members = query.offset(offset).limit(limit).all()
    return jsonify(members_schema.dump(members)), 200

# LOGIN (public)
@members_bp.post("/login")
def login_member():
    creds = request.get_json() or {}
    email = creds.get("email")
    password = creds.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    member = Member.query.filter_by(email=email).first()
    if member and check_password_hash(member.password, password):
        token = encode_token(member.id)
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "member": {
                "id": member.id,
                "name": member.name,
                "email": member.email
            },
            "token": token
        }), 200
    return jsonify({"message": "Email or password wrong"}), 401

# CREATE MEMBER (public, rate limited)
@members_bp.post("")
@limiter.limit("10 per hour")
def create_member():
    try:
        data = member_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    data.password = generate_password_hash(data.password)

    db.session.add(data)
    db.session.commit()
    cache.clear()
    return jsonify({
        "id": data.id,
        "name": data.name,
        "email": data.email,
        "created_at": data.created_at
    }), 201  

# GET ONE MEMBER
@members_bp.get("/<int:member_id>")
def get_member(member_id: int):
    m = Member.query.get_or_404(member_id)
    return jsonify({
        "id": m.id,
        "name": m.name,
        "email": m.email,
        "created_at": m.created_at
    }), 200

# DELETE OWN ACCOUNT
@members_bp.delete("/me")
@token_required
def delete_own_member(user_id):
    m = Member.query.get_or_404(user_id)
    db.session.delete(m)
    db.session.commit()
    cache.clear()
    return jsonify({"message": f"User {user_id} deleted"}), 200
