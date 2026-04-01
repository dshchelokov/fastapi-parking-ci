import pytest

from app import create_app, db


@pytest.fixture(scope="function")
def app():
    app = create_app("config.TestConfig")
    with app.app_context():
        db.engine.execute("DROP TABLE IF EXISTS client_parking")
        db.engine.execute("DROP TABLE IF EXISTS parking")
        db.engine.execute("DROP TABLE IF EXISTS client")
        db.create_all()
        yield app
        db.drop_all()
