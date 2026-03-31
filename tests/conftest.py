import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import create_app, database
from app.models import Client, Parking, ClientParking

@pytest.fixture(scope='function')
def app():
    app = create_app('config.TestConfig')
    with app.app_context():
        database.create_all()
        yield app
        database.drop_all()

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def db_session(app):
    return database.session