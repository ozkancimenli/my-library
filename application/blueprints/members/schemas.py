from application.extensions import ma
from application.models import Member

class MemberSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Member
        load_instance = True
        ordered = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    password = ma.auto_field(required=True, load_only=True)  # ✅ sadece input için
    created_at = ma.auto_field(dump_only=True)

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
