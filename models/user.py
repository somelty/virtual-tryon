import uuid
from datetime import datetime, timedelta
from models import db
from flask_bcrypt import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(64), unique=True)
    reset_token = db.Column(db.String(64), unique=True)
    reset_token_expiry = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    photos = db.relationship('Photo', backref='owner', lazy='dynamic',
                             cascade='all, delete-orphan')
    clothes = db.relationship('Clothing', backref='owner', lazy='dynamic',
                              cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_active_photo(self):
        return self.photos.filter_by(is_active=True).first()

    def generate_verification_token(self):
        self.verification_token = uuid.uuid4().hex
        return self.verification_token

    def generate_reset_token(self):
        self.reset_token = uuid.uuid4().hex
        self.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        return self.reset_token
