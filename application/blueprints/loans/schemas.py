from application.extensions import ma
from application.models import Loan
from application.blueprints.members.schemas import MemberSchema
from application.blueprints.books.schemas import BookSchema

class LoanSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Loan
        load_instance = True
        ordered = True

    id = ma.auto_field(dump_only=True)
    member_id = ma.auto_field(required=True)
    created_at = ma.auto_field(dump_only=True)

    member = ma.Nested(MemberSchema, dump_only=True)
    books = ma.Nested(BookSchema, many=True, dump_only=True)

loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)
