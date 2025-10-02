from application.extensions import ma
from application.models import Book

class BookSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Book
        load_instance = True
        ordered = True

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(required=True)
    author = ma.auto_field(required=True)
    created_at = ma.auto_field(dump_only=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)
