from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config
from models import db

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录。'


@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.query.get(int(user_id))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

    from blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)
    from blueprints.main import main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
