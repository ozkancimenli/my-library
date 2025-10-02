from flask import request, jsonify
from marshmallow import ValidationError
from application.extensions import db, limiter, cache
from application.models import Book
from . import books_bp
from .schemas import book_schema, books_schema

# GET ALL (with optional pagination)
@books_bp.get("")
@cache.cached(timeout=60)
def list_books():
    limit = request.args.get("limit", type=int)
    offset = request.args.get("offset", type=int)

    query = Book.query.order_by(Book.id.desc())
    if offset is not None:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)

    books = query.all()
    return jsonify(books_schema.dump(books)), 200

# CREATE
@books_bp.post("")
@limiter.limit("20 per hour")
def create_book():
    try:
        data = book_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.add(data)
    db.session.commit()
    cache.clear()
    return jsonify(book_schema.dump(data)), 201

# GET ONE
@books_bp.get("/<int:book_id>")
def get_book(book_id: int):
    b = Book.query.get_or_404(book_id)
    return jsonify(book_schema.dump(b)), 200

# UPDATE
@books_bp.put("/<int:book_id>")
def update_book(book_id: int):
    b = Book.query.get_or_404(book_id)
    payload = request.get_json() or {}
    if "title" in payload:
        b.title = payload["title"]
    if "author" in payload:
        b.author = payload["author"]
    db.session.commit()
    cache.clear()
    return jsonify(book_schema.dump(b)), 200

# DELETE
@books_bp.delete("/<int:book_id>")
def delete_book(book_id: int):
    b = Book.query.get_or_404(book_id)
    db.session.delete(b)
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Book deleted"}), 200

# SEARCH (query param)
@books_bp.get("/search")
def search_books():
    title = request.args.get("title", "")
    query = Book.query
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    results = query.all()
    return jsonify(books_schema.dump(results)), 200

# POPULAR BOOKS
@books_bp.get("/popular")
def popular_books():
    books = Book.query.all()
    books.sort(key=lambda b: len(b.loans), reverse=True)
    return jsonify([
        {"id": b.id, "title": b.title, "author": b.author, "loan_count": len(b.loans)}
        for b in books
    ]), 200
