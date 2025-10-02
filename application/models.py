from datetime import datetime
from .extensions import db

loan_books = db.Table(
    "loan_books",
    db.Column("loan_id", db.Integer, db.ForeignKey("loan.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
)

class Member(db.Model):
    __tablename__ = "member"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # ✅ Hash uzun olabilir, String(500) veya Text daha güvenli
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    loans = db.relationship("Loan", backref="member", lazy=True, cascade="all, delete")


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(220), nullable=False)
    author = db.Column(db.String(160), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    books = db.relationship(
        "Book",
        secondary=loan_books,
        lazy="subquery",
        backref=db.backref("loans", lazy=True),
    )
