from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

database = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    database.init_app(app)

    with app.app_context():
        database.create_all()

    from app.routes import api_blueprint
    app.register_blueprint(api_blueprint)

    return app
