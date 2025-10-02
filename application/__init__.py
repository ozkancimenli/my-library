from flask import Flask, jsonify
from .extensions import db, ma, limiter, cache
from . import models
from .blueprints.members import members_bp
from .blueprints.books import books_bp
from .blueprints.loans import loans_bp
from config import config

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # init extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    # register blueprints
    app.register_blueprint(members_bp, url_prefix="/members")
    app.register_blueprint(books_bp,   url_prefix="/books")
    app.register_blueprint(loans_bp,   url_prefix="/loans")

    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    return app
