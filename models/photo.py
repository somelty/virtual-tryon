from datetime import datetime
from models import db


class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def set_active(user_id, photo_id):
        """将指定 photo 设为激活，同一用户的其他 photo 取消激活"""
        Photo.query.filter_by(user_id=user_id, is_active=True).update({'is_active': False})
        photo = Photo.query.filter_by(id=photo_id, user_id=user_id).first()
        if photo:
            photo.is_active = True
            db.session.commit()
            return True
        return False


@db.event.listens_for(db.session, 'before_flush')
def _ensure_single_active_photo(session, flush_context, instances):
    """flush 前确保同一用户只有一个 active photo"""
    by_user = {}
    for obj in list(session.new):
        if isinstance(obj, Photo) and obj.is_active and obj.user_id:
            by_user.setdefault(obj.user_id, []).append(obj)

    for user_id, photos in by_user.items():
        if len(photos) > 1:
            for photo in photos[:-1]:
                photo.is_active = False
