import pytest

from app import create_app, db


@pytest.fixture(scope="session")
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def db_session(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
