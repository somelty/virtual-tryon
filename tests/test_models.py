import pytest
from models import db
from models.user import User
from models.photo import Photo
from models.clothing import Clothing
from datetime import datetime


class TestUserModel:
    def test_create_user(self, app):
        with app.app_context():
            user = User(username='alice', email='alice@test.com')
            user.set_password('secret')
            db.session.add(user)
            db.session.commit()

            fetched = User.query.filter_by(username='alice').first()
            assert fetched is not None
            assert fetched.email == 'alice@test.com'
            assert fetched.check_password('secret') is True
            assert fetched.check_password('wrong') is False
            assert fetched.email_verified is False
            assert fetched.created_at is not None

    def test_username_unique(self, app):
        with app.app_context():
            u1 = User(username='bob', email='bob1@test.com')
            u1.set_password('pw')
            u2 = User(username='bob', email='bob2@test.com')
            u2.set_password('pw')
            db.session.add(u1)
            db.session.commit()
            db.session.add(u2)
            with pytest.raises(Exception):
                db.session.commit()

    def test_email_unique(self, app):
        with app.app_context():
            u1 = User(username='c1', email='c@test.com')
            u1.set_password('pw')
            u2 = User(username='c2', email='c@test.com')
            u2.set_password('pw')
            db.session.add(u1)
            db.session.commit()
            db.session.add(u2)
            with pytest.raises(Exception):
                db.session.commit()


class TestPhotoModel:
    def test_create_photo(self, app):
        with app.app_context():
            user = User(username='puser', email='p@test.com')
            user.set_password('pw')
            db.session.add(user)
            db.session.commit()

            photo = Photo(user_id=user.id, filename='test.jpg')
            db.session.add(photo)
            db.session.commit()

            assert photo.is_active is False
            assert photo.uploaded_at is not None
            assert photo.user_id == user.id

    def test_only_one_active_photo(self, app):
        with app.app_context():
            user = User(username='ap', email='ap@test.com')
            user.set_password('pw')
            db.session.add(user)
            db.session.commit()

            p1 = Photo(user_id=user.id, filename='a.jpg', is_active=True)
            p2 = Photo(user_id=user.id, filename='b.jpg', is_active=True)
            db.session.add(p1)
            db.session.add(p2)
            db.session.commit()

            active = Photo.query.filter_by(user_id=user.id, is_active=True).all()
            assert len(active) == 1  # 最后设置的那个


class TestClothingModel:
    def test_create_clothing(self, app):
        with app.app_context():
            user = User(username='cuser', email='c@test.com')
            user.set_password('pw')
            db.session.add(user)
            db.session.commit()

            item = Clothing(user_id=user.id, filename='shirt.png', category='Shirt')
            db.session.add(item)
            db.session.commit()

            assert item.category == 'Shirt'
            assert item.manual_category is None
            assert item.display_category() == 'Shirt'

    def test_display_category_manual_override(self, app):
        with app.app_context():
            user = User(username='duser', email='d@test.com')
            user.set_password('pw')
            db.session.add(user)
            db.session.commit()

            item = Clothing(user_id=user.id, filename='x.png',
                           category='Shirt', manual_category='Coat')
            db.session.add(item)
            db.session.commit()

            assert item.display_category() == 'Coat'
