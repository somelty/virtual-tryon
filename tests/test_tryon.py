import io
import os
from PIL import Image
from models import db
from models.clothing import Clothing
from models.photo import Photo


def _make_test_image(w, h, color=(100, 150, 200)):
    img = Image.new('RGB', (w, h), color=color)
    buf = io.BytesIO()
    img.save(buf, 'PNG')
    buf.seek(0)
    return buf


class TestTryOn:
    def test_tryon_endpoint(self, logged_in_user, app):
        client, user = logged_in_user
        app.config['TRYON_ENGINE'] = 'simple'
        with app.app_context():
            photo = Photo(user_id=user.id, filename='test_photo.png', is_active=True)
            clothing = Clothing(user_id=user.id, filename='test_cloth.png', category='Shirt')
            db.session.add_all([photo, clothing])
            db.session.commit()
            cid = clothing.id

            user_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(user.id))
            os.makedirs(user_dir, exist_ok=True)
            Image.new('RGB', (200, 300), color='red').save(os.path.join(user_dir, 'test_photo.png'))
            Image.new('RGB', (100, 100), color='blue').save(os.path.join(user_dir, 'test_cloth.png'))

        response = client.post(f'/tryon/{cid}', follow_redirects=True)
        assert response.status_code == 200

    def test_tryon_no_active_photo(self, logged_in_user, app):
        client, user = logged_in_user
        with app.app_context():
            clothing = Clothing(user_id=user.id, filename='c.png', category='Shirt')
            db.session.add(clothing)
            db.session.commit()
            cid = clothing.id

        response = client.post(f'/tryon/{cid}', follow_redirects=True)
        assert response.status_code == 200
        assert '请先上传' in response.data.decode('utf-8')

    def test_tryon_other_user_clothing(self, logged_in_user, app):
        client, user = logged_in_user
        with app.app_context():
            from models.user import User
            other = User(username='tryon_other', email='to@test.com')
            other.set_password('pw')
            db.session.add(other)
            db.session.commit()
            clothing = Clothing(user_id=other.id, filename='x.png', category='Coat')
            db.session.add(clothing)
            db.session.commit()
            cid = clothing.id

        response = client.post(f'/tryon/{cid}', follow_redirects=True)
        assert response.status_code == 404
