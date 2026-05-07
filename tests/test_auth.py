from datetime import datetime, timedelta

import pytest
from models import db
from models.user import User


class TestRegister:
    def test_register_page_loads(self, client):
        response = client.get('/register')
        assert response.status_code == 200

    def test_register_success(self, client, app):
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'Password1',
            'confirm_password': 'Password1'
        })
        assert response.status_code == 302  # redirect to login
        with app.app_context():
            user = User.query.filter_by(username='newuser').first()
            assert user is not None
            assert user.email == 'new@example.com'
            assert user.email_verified is False
            assert user.verification_token is not None

    def test_register_duplicate_username(self, client, app):
        with app.app_context():
            user = User(username='dup', email='dup@test.com')
            user.set_password('pw')
            db.session.add(user)
            db.session.commit()

        response = client.post('/register', data={
            'username': 'dup',
            'email': 'other@test.com',
            'password': 'Password1',
            'confirm_password': 'Password1'
        })
        assert '用户名已被使用' in response.data.decode('utf-8') or response.status_code != 302

    def test_register_password_mismatch(self, client):
        response = client.post('/register', data={
            'username': 'mismatch',
            'email': 'mm@test.com',
            'password': 'Password1',
            'confirm_password': 'Different1'
        })
        assert response.status_code == 200  # stays on register page


class TestLogin:
    def test_login_page_loads(self, client):
        response = client.get('/login')
        assert response.status_code == 200

    def test_login_success(self, client, app):
        with app.app_context():
            user = User(username='loginuser', email='login@test.com',
                       email_verified=True)
            user.set_password('Password1')
            db.session.add(user)
            db.session.commit()

        response = client.post('/login', data={
            'email': 'login@test.com',
            'password': 'Password1'
        })
        assert response.status_code == 302  # redirect to main.index (or next)

    def test_login_wrong_password(self, client, app):
        with app.app_context():
            user = User(username='wrongpw', email='wrongpw@test.com',
                       email_verified=True)
            user.set_password('correct')
            db.session.add(user)
            db.session.commit()

        response = client.post('/login', data={
            'email': 'wrongpw@test.com',
            'password': 'wrongpassword'
        })
        assert '邮箱或密码错误' in response.data.decode('utf-8') or response.status_code != 302


class TestVerifyEmail:
    def test_verify_email_success(self, client, app):
        with app.app_context():
            user = User(username='vuser', email='v@test.com')
            user.set_password('pw')
            user.generate_verification_token()
            db.session.add(user)
            db.session.commit()
            token = user.verification_token

        response = client.get(f'/verify/{token}', follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            verified_user = User.query.filter_by(username='vuser').first()
            assert verified_user.email_verified is True
            assert verified_user.verification_token is None

    def test_verify_invalid_token(self, client):
        response = client.get('/verify/invalidtoken', follow_redirects=True)
        assert response.status_code == 200


class TestResetPassword:
    def test_reset_request_page_loads(self, client):
        response = client.get('/reset-password')
        assert response.status_code == 200

    def test_reset_request_creates_token(self, client, app):
        with app.app_context():
            user = User(username='ruser', email='r@test.com', email_verified=True)
            user.set_password('pw')
            db.session.add(user)
            db.session.commit()

        response = client.post('/reset-password', data={
            'email': 'r@test.com'
        }, follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            updated = User.query.filter_by(username='ruser').first()
            assert updated.reset_token is not None
            assert updated.reset_token_expiry is not None

    def test_reset_password_with_valid_token(self, client, app):
        with app.app_context():
            user = User(username='puser', email='p@test.com', email_verified=True)
            user.set_password('oldpw')
            user.reset_token = 'valid-token'
            user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
            db.session.add(user)
            db.session.commit()

        response = client.post('/reset-password', data={
            'token': 'valid-token',
            'password': 'NewPass1',
            'confirm_password': 'NewPass1'
        }, follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            updated = User.query.filter_by(username='puser').first()
            assert updated.check_password('NewPass1') is True
            assert updated.reset_token is None
