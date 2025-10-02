from flask import Flask, jsonify
from .extensions import db, ma, limiter, cache
from . import models
from .blueprints.members import members_bp
from .blueprints.books import books_bp
from .blueprints.loans import loans_bp
from .blueprints.items import items_bp
from .blueprints.orders import orders_bp
from config import config
from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Your API's Name"}
)


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
    app.register_blueprint(books_bp, url_prefix="/books")
    app.register_blueprint(loans_bp, url_prefix="/loans")
    app.register_blueprint(items_bp, url_prefix="/items")
    app.register_blueprint(orders_bp, url_prefix="/orders")
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    return app
