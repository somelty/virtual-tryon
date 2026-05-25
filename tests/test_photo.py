import io
import os
from PIL import Image
from models import db
from models.photo import Photo
from models.user import User


def _make_fake_image():
    """生成一个假的 PNG 图片 bytes"""
    img = Image.new('RGB', (100, 100), color='red')
    buf = io.BytesIO()
    img.save(buf, 'PNG')
    buf.seek(0)
    return buf


class TestPhotoUpload:
    def test_upload_photo(self, logged_in_user, app):
        client, user = logged_in_user
        fake_img = _make_fake_image()
        response = client.post('/upload-photo', data={
            'photos': (fake_img, 'myphoto.png')
        }, content_type='multipart/form-data', follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            photos = Photo.query.filter_by(user_id=user.id).all()
            assert len(photos) == 1
            assert photos[0].is_active is True  # first photo auto-activated

    def test_set_active_photo(self, logged_in_user, app):
        client, user = logged_in_user
        with app.app_context():
            p1 = Photo(user_id=user.id, filename='a.jpg', is_active=True)
            p2 = Photo(user_id=user.id, filename='b.jpg', is_active=False)
            db.session.add_all([p1, p2])
            db.session.commit()
            p1_id = p1.id
            p2_id = p2.id

        response = client.post(f'/set-photo/{p2_id}', follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            p1_after = db.session.get(Photo, p1_id)
            p2_after = db.session.get(Photo, p2_id)
            assert p1_after.is_active is False
            assert p2_after.is_active is True

    def test_cannot_access_other_user_photo(self, logged_in_user, app):
        client, user = logged_in_user
        with app.app_context():
            other = User(username='other', email='other@test.com')
            other.set_password('pw')
            db.session.add(other)
            db.session.commit()
            p = Photo(user_id=other.id, filename='x.jpg', is_active=True)
            db.session.add(p)
            db.session.commit()
            other_photo_id = p.id

        response = client.post(f'/set-photo/{other_photo_id}', follow_redirects=True)
        assert response.status_code == 404

    def test_delete_photo(self, logged_in_user, app):
        client, user = logged_in_user
        with app.app_context():
            p = Photo(user_id=user.id, filename='del.jpg', is_active=True)
            db.session.add(p)
            db.session.commit()
            pid = p.id

        response = client.post(f'/delete-photo/{pid}', follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            assert Photo.query.get(pid) is None
