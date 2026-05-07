import pytest
import os
import tempfile
from app import create_app
from models import db, User, Photo, Clothing


@pytest.fixture
def app():
    app = create_app('config.TestConfig')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def logged_in_user(app, client):
    """创建并登录一个用户，返回 (client, user)"""
    from models.user import User
    with app.app_context():
        user = User(username='testuser', email='test@example.com', email_verified=True)
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        return client, user
