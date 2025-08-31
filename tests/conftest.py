import pytest
from app import app as flask_app, db as sqlalchemy_db

@pytest.fixture(scope='module')
def app():
    """Create and configure a new app instance for each test module."""
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing forms

    with flask_app.app_context():
        sqlalchemy_db.create_all()
        yield flask_app
        sqlalchemy_db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='module')
def db(app):
    """A database for the app."""
    return sqlalchemy_db
