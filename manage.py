from application import create_app
from application.extensions import db

app = create_app("development")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully.")
