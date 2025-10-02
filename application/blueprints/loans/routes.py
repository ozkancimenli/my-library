from flask import request, jsonify
from marshmallow import ValidationError
from application.extensions import db, limiter, cache
from application.models import Loan, Member, Book
from . import loans_bp
from .schemas import loan_schema, loans_schema

# GET ALL
@loans_bp.get("")
@cache.cached(timeout=30)
def list_loans():
    loans = Loan.query.order_by(Loan.id.desc()).all()
    return jsonify(loans_schema.dump(loans)), 200

# CREATE
@loans_bp.post("")
@limiter.limit("15 per hour")
def create_loan():
    payload = request.get_json() or {}
    try:
        data = loan_schema.load({"member_id": payload.get("member_id")})
    except ValidationError as err:
        return jsonify(err.messages), 400

    member = Member.query.get(payload.get("member_id"))
    if not member:
        return jsonify({"message": "Member not found"}), 404

    loan = Loan(member_id=member.id)

    book_id = payload.get("book_id")
    if book_id:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({"message": "Book not found"}), 404
        loan.books.append(book)

    db.session.add(loan)
    db.session.commit()
    cache.clear()
    return jsonify(loan_schema.dump(loan)), 201

# GET ONE
@loans_bp.get("/<int:loan_id>")
def get_loan(loan_id: int):
    loan = Loan.query.get_or_404(loan_id)
    return jsonify(loan_schema.dump(loan)), 200

# EDIT BOOKS IN LOAN (add/remove in one request)
@loans_bp.put("/<int:loan_id>/edit")
def edit_loan_books(loan_id: int):
    loan = Loan.query.get_or_404(loan_id)
    payload = request.get_json() or {}

    add_ids = payload.get("add_ids", [])
    remove_ids = payload.get("remove_ids", [])

    for book_id in add_ids:
        book = Book.query.get(book_id)
        if book and book not in loan.books:
            loan.books.append(book)

    for book_id in remove_ids:
        book = Book.query.get(book_id)
        if book and book in loan.books:
            loan.books.remove(book)

    db.session.commit()
    cache.clear()
    return jsonify(loan_schema.dump(loan)), 200
