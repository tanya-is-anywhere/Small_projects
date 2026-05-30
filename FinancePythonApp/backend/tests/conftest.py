import pytest
from app import create_app, db as _db

TEST_DATABASE_URL = 'sqlite:///:memory:'


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URL,
        'JWT_SECRET_KEY': 'test-secret-key85638542test-secret-key',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'testpass123'
    })

    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass123'
    })

    token = response.json['token']
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
