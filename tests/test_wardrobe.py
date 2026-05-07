import io
import os
from PIL import Image
from models import db
from models.clothing import Clothing


def _make_fake_clothing():
    img = Image.new('RGB', (28, 28), color='blue')
    buf = io.BytesIO()
    img.save(buf, 'PNG')
    buf.seek(0)
    return buf


class TestWardrobe:
    def test_wardrobe_page(self, logged_in_user, app):
        client, user = logged_in_user
        response = client.get('/wardrobe')
        assert response.status_code == 200

    def test_upload_clothing(self, logged_in_user, app):
        client, user = logged_in_user
        fake_img = _make_fake_clothing()
        response = client.post('/wardrobe/upload', data={
            'clothing': (fake_img, 'shirt.png')
        }, content_type='multipart/form-data', follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            items = Clothing.query.filter_by(user_id=user.id).all()
            assert len(items) == 1
            assert items[0].category != ''  # CNN should classify

    def test_edit_category(self, logged_in_user, app):
        client, user = logged_in_user
        with app.app_context():
            item = Clothing(user_id=user.id, filename='test.png', category='Shirt')
            db.session.add(item)
            db.session.commit()
            cid = item.id

        response = client.post(f'/wardrobe/{cid}/edit', data={
            'manual_category': 'Coat'
        }, follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            updated = Clothing.query.get(cid)
            assert updated.manual_category == 'Coat'
            assert updated.display_category() == 'Coat'

    def test_delete_clothing(self, logged_in_user, app):
        client, user = logged_in_user
        with app.app_context():
            item = Clothing(user_id=user.id, filename='del.png', category='Bag')
            db.session.add(item)
            db.session.commit()
            cid = item.id

        response = client.post(f'/wardrobe/{cid}/delete', follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            assert Clothing.query.get(cid) is None

    def test_cannot_access_other_user_clothing(self, logged_in_user, app):
        client, user = logged_in_user
        with app.app_context():
            from models.user import User
            other = User(username='wardrobe_other', email='wo@test.com')
            other.set_password('pw')
            db.session.add(other)
            db.session.commit()
            item = Clothing(user_id=other.id, filename='x.png', category='Bag')
            db.session.add(item)
            db.session.commit()
            cid = item.id

        response = client.post(f'/wardrobe/{cid}/edit', data={
            'manual_category': 'Coat'
        }, follow_redirects=True)
        assert response.status_code == 404
