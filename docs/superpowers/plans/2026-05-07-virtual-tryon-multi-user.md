# 虚拟试衣多用户系统 — 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将当前单页 Flask Demo 升级为支持多用户的虚拟试衣系统，含注册登录、照片管理、衣物库管理、MediaPipe 虚拟试穿。

**Architecture:** Flask 工厂模式 + 4 个 Blueprint（auth/main/wardrobe/tryon），SQLAlchemy ORM + SQLite，TryOnEngine 抽象接口（SimpleEngine 回退 + MediaPipeEngine 默认），Jinja2 模板 + Vanilla JS 前端。

**Tech Stack:** Python 3.12, Flask 3.1, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt, PyTorch 2.x, MediaPipe, OpenCV, Pillow, SQLite, pytest

---

### 文件结构总览

```
Create:  config.py, models/__init__.py, models/user.py, models/photo.py, models/clothing.py
Create:  blueprints/__init__.py, blueprints/auth.py, blueprints/main.py, blueprints/wardrobe.py, blueprints/tryon.py
Create:  engines/__init__.py, engines/base.py, engines/simple.py, engines/mediapipe.py
Create:  utils/__init__.py, utils/email.py, utils/image.py
Create:  templates/base.html, templates/login.html, templates/register.html, templates/reset_password.html, templates/wardrobe.html
Create:  tests/conftest.py, tests/test_models.py, tests/test_auth.py, tests/test_photo.py, tests/test_wardrobe.py, tests/test_tryon.py
Modify:  app.py, templates/index.html
```

---

### Task 1: 项目基础设施

**Files:**
- Create: `config.py`, `tests/conftest.py`
- Modify: `app.py`

- [ ] **Step 1: 安装新依赖**

```bash
source venv/Scripts/activate && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple flask-login flask-bcrypt flask-sqlalchemy flask-wtf opencv-python mediapipe pytest
```

Expected: 所有包安装成功，无错误。

- [ ] **Step 2: 创建 config.py**

```python
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    RESULT_FOLDER = os.path.join(BASE_DIR, 'static', 'results')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    TRYON_ENGINE = 'mediapipe'  # 'mediapipe' | 'simple'


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost'
```

- [ ] **Step 3: 创建 tests/conftest.py**

```python
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
```

- [ ] **Step 4: 运行测试验证基础设施就绪**

```bash
source venv/Scripts/activate && python -m pytest tests/conftest.py -v
```

Expected: 无错误（0 个测试被收集，但导入无报错）。

- [ ] **Step 5: 备份现有 app.py 并改造为工厂函数框架**

现有 `app.py` 重命名为 `app_old.py` 作为参考。

```python
from flask import Flask
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展 (后续任务添加)
    # 注册蓝图 (后续任务添加)

    # 确保上传和结果目录存在
    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
```

- [ ] **Step 6: 验证 Flask 能正常启动**

```bash
source venv/Scripts/activate && timeout 3 python app.py 2>&1 || true
```

Expected: 看到 "Running on http://127.0.0.1:5000" (或类似)，无 import 错误。

---

### Task 2: 数据模型

**Files:**
- Create: `models/__init__.py`, `models/user.py`, `models/photo.py`, `models/clothing.py`
- Create: `tests/test_models.py`

- [ ] **Step 1: 编写模型测试（先写测试，验证能失败）**

```python
# tests/test_models.py
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
```

- [ ] **Step 2: 运行测试，验证失败**

```bash
source venv/Scripts/activate && python -m pytest tests/test_models.py -v
```

Expected: FAIL — ModuleNotFoundError for models

- [ ] **Step 3: 创建 models/__init__.py + models/user.py**

```python
# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User
from models.photo import Photo
from models.clothing import Clothing
```

```python
# models/user.py
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
```

- [ ] **Step 4: 创建 models/photo.py**

```python
# models/photo.py
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
```

- [ ] **Step 5: 创建 models/clothing.py**

```python
# models/clothing.py
from datetime import datetime
from models import db


class Clothing(db.Model):
    __tablename__ = 'clothes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), default='')
    manual_category = db.Column(db.String(50), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def display_category(self):
        return self.manual_category or self.category
```

- [ ] **Step 6: 运行测试，验证全部通过**

```bash
source venv/Scripts/activate && python -m pytest tests/test_models.py -v
```

Expected: 7 tests PASS

---

### Task 3: 用户注册

**Files:**
- Create: `blueprints/auth.py`
- Create: `tests/test_auth.py`
- Modify: `app.py` (注册 auth blueprint + 初始化扩展)

- [ ] **Step 1: 编写注册测试**

```python
# tests/test_auth.py
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
        }, follow_redirects=True)
        assert response.status_code == 200
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
        assert response.status_code == 200  # 停留在注册页面


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
        }, follow_redirects=True)
        assert response.status_code == 200

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
```

- [ ] **Step 2: 运行测试，验证失败**

```bash
source venv/Scripts/activate && python -m pytest tests/test_auth.py -v
```

Expected: FAIL — 路由不存在

- [ ] **Step 3: 更新 app.py 集成 Flask-SQLAlchemy + Flask-Bcrypt + Flask-Login**

```python
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

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
```

- [ ] **Step 4: 创建 blueprints/auth.py — 注册路由**

```python
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        errors = []
        if not username or len(username) < 2:
            errors.append('用户名至少2个字符')
        if not email or '@' not in email:
            errors.append('请输入有效的邮箱')
        if len(password) < 6:
            errors.append('密码至少6个字符')
        if password != confirm_password:
            errors.append('两次密码不一致')

        if User.query.filter_by(username=username).first():
            errors.append('用户名已被使用')
        if User.query.filter_by(email=email).first():
            errors.append('邮箱已被注册')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('register.html')

        user = User(username=username, email=email)
        user.set_password(password)
        user.generate_verification_token()
        db.session.add(user)
        db.session.commit()

        # 开发阶段：打印验证链接到控制台
        print(f'\n[DEV] 邮箱验证链接: http://localhost:5000/verify/{user.verification_token}\n')
        flash('注册成功！验证邮件已发送（开发模式请查看控制台）', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')
```

- [ ] **Step 5: 运行注册测试**

```bash
source venv/Scripts/activate && python -m pytest tests/test_auth.py::TestRegister -v
```

Expected: 4 tests PASS

---

### Task 4: 登录/退出

**Files:**
- Modify: `blueprints/auth.py` (添加 login/logout 路由)
- Create: `templates/login.html`, `templates/register.html`

- [ ] **Step 1: 创建 templates/register.html（最简可测试版）**

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="utf-8">
  <title>注册 - FitAI</title>
</head>
<body>
  <h1>注册</h1>
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      {% for category, message in messages %}
        <p class="{{ category }}">{{ message }}</p>
      {% endfor %}
    {% endif %}
  {% endwith %}
  <form method="post">
    <input type="text" name="username" placeholder="用户名" required>
    <input type="email" name="email" placeholder="邮箱" required>
    <input type="password" name="password" placeholder="密码" required>
    <input type="password" name="confirm_password" placeholder="确认密码" required>
    <button type="submit">注册</button>
  </form>
  <p>已有账号？<a href="{{ url_for('auth.login') }}">登录</a></p>
</body>
</html>
```

- [ ] **Step 2: 创建 templates/login.html（最简可测试版）**

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="utf-8">
  <title>登录 - FitAI</title>
</head>
<body>
  <h1>登录</h1>
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      {% for category, message in messages %}
        <p class="{{ category }}">{{ message }}</p>
      {% endfor %}
    {% endif %}
  {% endwith %}
  <form method="post">
    <input type="email" name="email" placeholder="邮箱" required>
    <input type="password" name="password" placeholder="密码" required>
    <button type="submit">登录</button>
  </form>
  <p>没有账号？<a href="{{ url_for('auth.register') }}">注册</a></p>
  <p><a href="{{ url_for('auth.reset_password') }}">忘记密码？</a></p>
</body>
</html>
```

- [ ] **Step 3: 向 blueprints/auth.py 添加 login/logout 路由**

```python
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        flash('邮箱或密码错误', 'error')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录', 'info')
    return redirect(url_for('auth.login'))
```

- [ ] **Step 4: 运行全部 auth 测试**

```bash
source venv/Scripts/activate && python -m pytest tests/test_auth.py -v
```

Expected: 7 tests PASS

---

### Task 5: 邮箱验证 + 密码重置

**Files:**
- Create: `utils/__init__.py`, `utils/email.py`
- Modify: `blueprints/auth.py`
- Modify: `tests/test_auth.py`

- [ ] **Step 1: 编写邮箱验证测试**

```python
# 追加到 tests/test_auth.py
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
```

- [ ] **Step 2: 运行测试，验证失败**

```bash
source venv/Scripts/activate && python -m pytest tests/test_auth.py -v
```

Expected: FAIL — 3 tests 失败（验证和重置路由不存在）

- [ ] **Step 3: 创建 utils/email.py**

```python
def send_verification_email(user, token):
    link = f'http://localhost:5000/verify/{token}'
    print(f'\n===== 验证邮件 =====')
    print(f'收件人: {user.email}')
    print(f'验证链接: {link}')
    print(f'====================\n')


def send_reset_email(user, token):
    link = f'http://localhost:5000/reset-password?token={token}'
    print(f'\n===== 密码重置邮件 =====')
    print(f'收件人: {user.email}')
    print(f'重置链接: {link}')
    print(f'========================\n')
```

- [ ] **Step 4: 向 blueprints/auth.py 添加 verify 和 reset-password 路由**

```python
from utils.email import send_verification_email, send_reset_email
from datetime import datetime


@auth_bp.route('/verify/<token>')
def verify_email(token):
    user = User.query.filter_by(verification_token=token).first()
    if user:
        user.email_verified = True
        user.verification_token = None
        db.session.commit()
        flash('邮箱验证成功，请登录', 'success')
    else:
        flash('验证链接无效或已过期', 'error')
    return redirect(url_for('auth.login'))


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    token = request.args.get('token')

    if request.method == 'POST':
        if token:
            # 第二步：设置新密码
            user = User.query.filter_by(reset_token=token).first()
            if user and user.reset_token_expiry and user.reset_token_expiry > datetime.utcnow():
                password = request.form.get('password', '')
                confirm = request.form.get('confirm_password', '')
                if len(password) < 6:
                    flash('密码至少6个字符', 'error')
                elif password != confirm:
                    flash('两次密码不一致', 'error')
                else:
                    user.set_password(password)
                    user.reset_token = None
                    user.reset_token_expiry = None
                    db.session.commit()
                    flash('密码已重置，请登录', 'success')
                    return redirect(url_for('auth.login'))
            else:
                flash('重置链接已过期', 'error')
                return redirect(url_for('auth.reset_password'))
        else:
            # 第一步：发送重置邮件
            email = request.form.get('email', '').strip()
            user = User.query.filter_by(email=email).first()
            if user:
                t = user.generate_reset_token()
                db.session.commit()
                send_reset_email(user, t)
            flash('如果该邮箱已注册，重置邮件已发送', 'info')
            return redirect(url_for('auth.login'))

    return render_template('reset_password.html', token=token)
```

- [ ] **Step 5: 创建 templates/reset_password.html（最简版）**

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="utf-8">
  <title>重置密码 - FitAI</title>
</head>
<body>
  <h1>重置密码</h1>
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      {% for category, message in messages %}
        <p class="{{ category }}">{{ message }}</p>
      {% endfor %}
    {% endif %}
  {% endwith %}
  {% if token %}
    <form method="post">
      <input type="hidden" name="token" value="{{ token }}">
      <input type="password" name="password" placeholder="新密码" required>
      <input type="password" name="confirm_password" placeholder="确认新密码" required>
      <button type="submit">重置密码</button>
    </form>
  {% else %}
    <form method="post">
      <input type="email" name="email" placeholder="注册邮箱" required>
      <button type="submit">发送重置链接</button>
    </form>
  {% endif %}
  <p><a href="{{ url_for('auth.login') }}">返回登录</a></p>
</body>
</html>
```

- [ ] **Step 6: 运行全部 auth 测试**

```bash
source venv/Scripts/activate && python -m pytest tests/test_auth.py -v
```

Expected: 10 tests PASS

---

### Task 6: 用户照片管理

**Files:**
- Create: `blueprints/main.py`, `utils/image.py`
- Create: `tests/test_photo.py`
- Modify: `app.py` (注册 main blueprint)

- [ ] **Step 1: 编写照片管理测试**

```python
# tests/test_photo.py
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
            'photo': (fake_img, 'myphoto.png')
        }, content_type='multipart/form-data', follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            photos = Photo.query.filter_by(user_id=user.id).all()
            assert len(photos) == 1
            assert photos[0].is_active is True  # 第一张自动激活

    def test_set_active_photo(self, logged_in_user, app):
        client, user = logged_in_user
        with app.app_context():
            p1 = Photo(user_id=user.id, filename='a.jpg', is_active=True)
            p2 = Photo(user_id=user.id, filename='b.jpg', is_active=False)
            db.session.add_all([p1, p2])
            db.session.commit()
            p2_id = p2.id

        response = client.post(f'/set-photo/{p2_id}', follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            p1_after = Photo.query.get(p1.id)
            p2_after = Photo.query.get(p2_id)
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
```

- [ ] **Step 2: 运行测试，验证失败**

```bash
source venv/Scripts/activate && python -m pytest tests/test_photo.py -v
```

Expected: FAIL — main blueprint 未注册

- [ ] **Step 3: 创建 utils/image.py**

```python
import os
import uuid
from PIL import Image
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_upload(file, upload_folder, subfolder=''):
    """保存上传文件，返回存储的文件名"""
    ext = file.filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    dest_dir = os.path.join(upload_folder, subfolder)
    os.makedirs(dest_dir, exist_ok=True)
    filepath = os.path.join(dest_dir, unique_name)
    img = Image.open(file)
    img = img.convert('RGB')
    img.save(filepath)
    return unique_name


def validate_image(file):
    """验证上传文件是否为有效图片"""
    if not file or file.filename == '':
        return False, '未选择文件'
    if not allowed_file(file.filename):
        return False, '不支持的图片格式'
    try:
        img = Image.open(file)
        img.verify()
        file.seek(0)
        return True, ''
    except Exception:
        return False, '无效的图片文件'
```

- [ ] **Step 4: 创建 blueprints/main.py**

```python
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from models import db
from models.photo import Photo
from utils.image import validate_image, save_upload

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def index():
    photos = Photo.query.filter_by(user_id=current_user.id).order_by(Photo.uploaded_at.desc()).all()
    active_photo = Photo.query.filter_by(user_id=current_user.id, is_active=True).first()
    return render_template('index.html', photos=photos, active_photo=active_photo)


@main_bp.route('/upload-photo', methods=['POST'])
@login_required
def upload_photo():
    file = request.files.get('photo')
    valid, msg = validate_image(file)
    if not valid:
        flash(msg, 'error')
        return redirect(url_for('main.index'))

    filename = save_upload(file, current_app.config['UPLOAD_FOLDER'],
                          subfolder=str(current_user.id))
    photo = Photo(user_id=current_user.id, filename=filename)
    # 第一张照片自动激活，或有激活的照片则保持
    existing_active = Photo.query.filter_by(user_id=current_user.id, is_active=True).first()
    if not existing_active:
        photo.is_active = True
    db.session.add(photo)
    db.session.commit()
    flash('照片上传成功', 'success')
    return redirect(url_for('main.index'))


@main_bp.route('/set-photo/<int:photo_id>', methods=['POST'])
@login_required
def set_active_photo(photo_id):
    success = Photo.set_active(current_user.id, photo_id)
    if not success:
        abort(404)
    flash('已切换试穿照片', 'success')
    return redirect(url_for('main.index'))


@main_bp.route('/delete-photo/<int:photo_id>', methods=['POST'])
@login_required
def delete_photo(photo_id):
    photo = Photo.query.filter_by(id=photo_id, user_id=current_user.id).first()
    if not photo:
        abort(404)
    was_active = photo.is_active
    db.session.delete(photo)
    db.session.commit()
    # 如果删除的是激活照片，自动激活最新的一张
    if was_active:
        latest = Photo.query.filter_by(user_id=current_user.id).order_by(Photo.uploaded_at.desc()).first()
        if latest:
            latest.is_active = True
            db.session.commit()
    flash('照片已删除', 'info')
    return redirect(url_for('main.index'))
```

- [ ] **Step 5: 在 app.py 注册 main blueprint**

```python
from blueprints.main import main_bp
app.register_blueprint(main_bp)
```

- [ ] **Step 6: 运行照片管理测试**

```bash
source venv/Scripts/activate && python -m pytest tests/test_photo.py -v
```

Expected: 4 tests PASS

---

### Task 7: 衣物库 CRUD

**Files:**
- Create: `blueprints/wardrobe.py`
- Create: `tests/test_wardrobe.py`
- Modify: `app.py` (注册 wardrobe blueprint)

- [ ] **Step 1: 编写衣橱测试**

```python
# tests/test_wardrobe.py
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
            assert items[0].category != ''  # CNN 应该给出了分类

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
```

- [ ] **Step 2: 运行测试，验证失败**

```bash
source venv/Scripts/activate && python -m pytest tests/test_wardrobe.py -v
```

Expected: FAIL — wardrobe blueprint 未注册

- [ ] **Step 3: 创建 blueprints/wardrobe.py**

```python
import os
import torch
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from torchvision import transforms
from PIL import Image
from models import db
from models.clothing import Clothing
from model import FashionCNN
from utils.image import validate_image, save_upload

wardrobe_bp = Blueprint('wardrobe', __name__, url_prefix='/wardrobe')

# FashionMNIST 类别
CLASSES = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
           'Sandal', 'Shirt', 'Sneaker', 'Ankle boot', 'Bag']

# 预加载 CNN 模型和预处理 pipeline
CNN_MODEL = None
CNN_PREPROCESS = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])


def _get_cnn_model():
    global CNN_MODEL
    if CNN_MODEL is None:
        CNN_MODEL = FashionCNN()
        CNN_MODEL.load_state_dict(torch.load('./cnn_model.pth',
                                             map_location=torch.device('cpu'),
                                             weights_only=True))
        CNN_MODEL.eval()
    return CNN_MODEL


def _classify_image(filepath):
    """对文件路径中的图片运行 CNN 分类，返回类别名"""
    model = _get_cnn_model()
    img = Image.open(filepath)
    tensor = CNN_PREPROCESS(img).unsqueeze(0)
    with torch.inference_mode():
        outputs = model(tensor)
        predicted = torch.argmax(outputs, dim=1)
    return CLASSES[predicted.item()]


@wardrobe_bp.route('')
@login_required
def index():
    items = Clothing.query.filter_by(user_id=current_user.id).order_by(Clothing.uploaded_at.desc()).all()
    return render_template('wardrobe.html', items=items, classes=CLASSES)


@wardrobe_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files.get('clothing')
    valid, msg = validate_image(file)
    if not valid:
        flash(msg, 'error')
        return redirect(url_for('wardrobe.index'))

    filename = save_upload(file, current_app.config['UPLOAD_FOLDER'],
                          subfolder=str(current_user.id))
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'],
                           str(current_user.id), filename)
    category = _classify_image(filepath)

    item = Clothing(user_id=current_user.id, filename=filename, category=category)
    db.session.add(item)
    db.session.commit()
    flash(f'衣物上传成功！AI 识别为: {category}', 'success')
    return redirect(url_for('wardrobe.index'))


@wardrobe_bp.route('/<int:item_id>/edit', methods=['POST'])
@login_required
def edit(item_id):
    item = Clothing.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not item:
        abort(404)
    item.manual_category = request.form.get('manual_category', '').strip() or None
    db.session.commit()
    flash('分类已更新', 'success')
    return redirect(url_for('wardrobe.index'))


@wardrobe_bp.route('/<int:item_id>/delete', methods=['POST'])
@login_required
def delete(item_id):
    item = Clothing.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not item:
        abort(404)
    # 删除服务器上的文件
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'],
                           str(current_user.id), item.filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    db.session.delete(item)
    db.session.commit()
    flash('衣物已删除', 'info')
    return redirect(url_for('wardrobe.index'))
```

- [ ] **Step 4: 在 app.py 注册 wardrobe blueprint**

```python
from blueprints.wardrobe import wardrobe_bp
app.register_blueprint(wardrobe_bp)
```

- [ ] **Step 5: 运行衣橱测试**

```bash
source venv/Scripts/activate && python -m pytest tests/test_wardrobe.py -v
```

Expected: 5 tests PASS

---

### Task 8: 虚拟试穿引擎 + 试穿路由

**Files:**
- Create: `engines/__init__.py`, `engines/base.py`, `engines/simple.py`, `engines/mediapipe.py`
- Create: `blueprints/tryon.py`
- Create: `tests/test_tryon.py`
- Modify: `app.py` (注册 tryon blueprint)

- [ ] **Step 1: 编写试穿引擎测试**

```python
# tests/test_tryon.py
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
        with app.app_context():
            photo = Photo(user_id=user.id, filename='test_photo.png',
                         is_active=True)
            clothing = Clothing(user_id=user.id, filename='test_cloth.png',
                               category='Shirt')
            db.session.add_all([photo, clothing])
            db.session.commit()
            cid = clothing.id

            # 在磁盘上创建测试文件
            user_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(user.id))
            os.makedirs(user_dir, exist_ok=True)
            Image.new('RGB', (200, 300), color='red').save(
                os.path.join(user_dir, 'test_photo.png'))
            Image.new('RGB', (100, 100), color='blue').save(
                os.path.join(user_dir, 'test_cloth.png'))

        response = client.post(f'/tryon/{cid}', follow_redirects=True)
        assert response.status_code == 200

    def test_tryon_no_active_photo(self, logged_in_user, app):
        client, user = logged_in_user
        with app.app_context():
            clothing = Clothing(user_id=user.id, filename='c.png',
                               category='Shirt')
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
            clothing = Clothing(user_id=other.id, filename='x.png',
                               category='Coat')
            db.session.add(clothing)
            db.session.commit()
            cid = clothing.id

        response = client.post(f'/tryon/{cid}', follow_redirects=True)
        assert response.status_code == 404
```

- [ ] **Step 2: 运行测试，验证失败**

```bash
source venv/Scripts/activate && python -m pytest tests/test_tryon.py -v
```

Expected: FAIL — tryon blueprint 未注册

- [ ] **Step 3: 创建 engines/__init__.py + engines/base.py**

```python
# engines/__init__.py
from engines.base import TryOnEngine
from engines.simple import SimpleEngine
from engines.mediapipe import MediaPipeEngine


def get_engine(engine_name):
    """根据配置名返回对应的引擎实例"""
    engines = {
        'simple': SimpleEngine(),
        'mediapipe': MediaPipeEngine(),
    }
    return engines.get(engine_name, MediaPipeEngine())
```

```python
# engines/base.py
from abc import ABC, abstractmethod
from PIL import Image


class TryOnEngine(ABC):
    @abstractmethod
    def composite(self, user_photo: Image.Image, clothing: Image.Image,
                  category: str) -> Image.Image:
        """将衣物合成到用户照片上，返回 RGBA 图片"""
        pass
```

- [ ] **Step 4: 创建 engines/simple.py**

```python
from engines.base import TryOnEngine


class SimpleEngine(TryOnEngine):
    """固定坐标粘贴引擎，用于回退"""

    REGION_MAPPING = {
        'T-shirt/top': (220, 150, 380, 330),
        'Pullover': (220, 150, 380, 330),
        'Dress': (210, 150, 390, 600),
        'Coat': (220, 150, 380, 360),
        'Shirt': (220, 150, 380, 330),
        'Trouser': (240, 330, 360, 680),
        'Sandal': [(250, 680, 280, 720), (320, 680, 350, 720)],
        'Sneaker': [(250, 680, 280, 720), (320, 680, 350, 720)],
        'Ankle boot': [(250, 680, 280, 720), (320, 680, 350, 720)],
        'Bag': (140, 280, 220, 400),
    }

    def composite(self, user_photo, clothing, category):
        # 缩放用户照片到标准尺寸
        user_photo = user_photo.resize((600, 800)).convert("RGBA")
        clothing = clothing.convert("RGBA")
        clothing.putalpha(230)

        region = self.REGION_MAPPING.get(category)
        if region is None:
            return user_photo

        if isinstance(region, list):
            for r in region:
                fitted = self._fit(clothing, r)
                user_photo.paste(fitted, r[:2], fitted)
        else:
            fitted = self._fit(clothing, region)
            user_photo.paste(fitted, region[:2], fitted)

        return user_photo

    def _fit(self, img, region):
        tw = region[2] - region[0]
        th = region[3] - region[1]
        return img.resize((tw, th))
```

- [ ] **Step 5: 创建 engines/mediapipe.py**

```python
import numpy as np
import cv2
from PIL import Image
from engines.base import TryOnEngine


class MediaPipeEngine(TryOnEngine):
    """MediaPipe Pose 关键点引擎"""

    # 从 MediaPipe Pose 获得的关键点索引
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    LEFT_WRIST = 15
    RIGHT_WRIST = 16

    def __init__(self):
        self._pose = None

    @property
    def pose(self):
        if self._pose is None:
            import mediapipe as mp
            self._pose = mp.solutions.pose.Pose(
                static_image_mode=True,
                model_complexity=1,
                enable_segmentation=False
            )
        return self._pose

    def _detect_keypoints(self, image):
        """返回 (keypoints_dict, image_width, image_height) 或 (None, None, None)"""
        img_rgb = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2RGB)
        results = self.pose.process(img_rgb)
        if not results.pose_landmarks:
            return None, None, None
        h, w = img_rgb.shape[:2]
        kp = {}
        for idx, lm in enumerate(results.pose_landmarks.landmark):
            kp[idx] = (int(lm.x * w), int(lm.y * h))
        return kp, w, h

    def _get_region_for_category(self, keypoints, category, img_w, img_h):
        """根据检测到的关键点和类别计算粘贴区域 (x1, y1, x2, y2)"""

        def midpoint(a, b):
            return ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)

        upper_categories = {'T-shirt/top', 'Pullover', 'Shirt', 'Coat', 'Dress'}
        lower_categories = {'Trouser'}
        shoe_categories = {'Sandal', 'Sneaker', 'Ankle boot'}
        bag_categories = {'Bag'}

        if category in upper_categories:
            if self.LEFT_SHOULDER in keypoints and self.RIGHT_SHOULDER in keypoints:
                shoulder_mid = midpoint(keypoints[self.LEFT_SHOULDER],
                                       keypoints[self.RIGHT_SHOULDER])
                x1 = max(0, shoulder_mid[0] - 120)
                x2 = min(img_w, shoulder_mid[0] + 120)
                y1 = max(0, shoulder_mid[1] - 20)
                if self.LEFT_HIP in keypoints and self.RIGHT_HIP in keypoints:
                    hip_mid = midpoint(keypoints[self.LEFT_HIP],
                                      keypoints[self.RIGHT_HIP])
                    y2 = hip_mid[1]
                else:
                    y2 = min(img_h, y1 + 250)
                return (x1, y1, x2, y2)
            # 回退：用固定坐标
            return (220, 150, 380, 330) if category != 'Dress' else (210, 150, 390, 600)

        if category in lower_categories:
            if all(k in keypoints for k in [self.LEFT_HIP, self.RIGHT_HIP]):
                hip_mid = midpoint(keypoints[self.LEFT_HIP], keypoints[self.RIGHT_HIP])
                x1 = max(0, hip_mid[0] - 100)
                x2 = min(img_w, hip_mid[0] + 100)
                y1 = hip_mid[1]
                if self.LEFT_ANKLE in keypoints and self.RIGHT_ANKLE in keypoints:
                    ankle_mid = midpoint(keypoints[self.LEFT_ANKLE],
                                        keypoints[self.RIGHT_ANKLE])
                    y2 = ankle_mid[1]
                else:
                    y2 = min(img_h, y1 + 350)
                return (x1, y1, x2, y2)
            return (240, 330, 360, 680)

        if category in shoe_categories:
            regions = []
            for ankle_idx in [self.LEFT_ANKLE, self.RIGHT_ANKLE]:
                if ankle_idx in keypoints:
                    a = keypoints[ankle_idx]
                    regions.append((max(0, a[0] - 30), a[1] - 20,
                                   min(img_w, a[0] + 30), min(img_h, a[1] + 40)))
            if regions:
                return regions
            return [(250, 680, 280, 720), (320, 680, 350, 720)]

        if category in bag_categories:
            if self.LEFT_WRIST in keypoints:
                w = keypoints[self.LEFT_WRIST]
                return (max(0, w[0] - 60), max(0, w[1] - 40),
                       min(img_w, w[0] + 60), min(img_h, w[1] + 80))
            return (140, 280, 220, 400)

        return None

    def composite(self, user_photo, clothing, category):
        user_photo = user_photo.convert("RGBA")
        clothing = clothing.convert("RGBA")
        clothing.putalpha(200)

        keypoints, img_w, img_h = self._detect_keypoints(user_photo)

        if keypoints is None:
            # 关键点检测失败，回到固定坐标
            from engines.simple import SimpleEngine
            return SimpleEngine().composite(user_photo, clothing, category)

        region = self._get_region_for_category(keypoints, category, img_w, img_h)

        if region is None:
            return user_photo

        if isinstance(region, list):
            for r in region:
                fitted = self._affine_fit(clothing, r)
                user_photo.paste(fitted, r[:2], fitted)
        else:
            fitted = self._affine_fit(clothing, region)
            user_photo.paste(fitted, region[:2], fitted)

        return user_photo

    def _affine_fit(self, img, region):
        """将衣物图片仿射变换适配目标区域"""
        tw = region[2] - region[0]
        th = region[3] - region[1]
        if tw <= 0 or th <= 0:
            return img
        src_pts = np.float32([[0, 0], [img.width, 0], [0, img.height]])
        dst_pts = np.float32([[0, 0], [tw, 0], [0, th]])
        matrix = cv2.getAffineTransform(src_pts, dst_pts)
        warped = cv2.warpAffine(np.array(img), matrix, (tw, th),
                                flags=cv2.INTER_LANCZOS4)
        return Image.fromarray(warped, 'RGBA')
```

- [ ] **Step 6: 创建 blueprints/tryon.py**

```python
import os
from flask import Blueprint, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from PIL import Image
from models import db
from models.clothing import Clothing
from models.photo import Photo
from engines import get_engine

tryon_bp = Blueprint('tryon', __name__, url_prefix='/tryon')


@tryon_bp.route('/<int:clothing_id>', methods=['POST'])
@login_required
def try_on(clothing_id):
    clothing = Clothing.query.filter_by(id=clothing_id, user_id=current_user.id).first()
    if not clothing:
        abort(404)

    active_photo = Photo.query.filter_by(user_id=current_user.id, is_active=True).first()
    if not active_photo:
        flash('请先上传个人照片并设为当前试穿底图', 'error')
        return redirect(url_for('main.index'))

    user_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], str(current_user.id))
    photo_path = os.path.join(user_dir, active_photo.filename)
    cloth_path = os.path.join(user_dir, clothing.filename)

    user_photo = Image.open(photo_path)
    cloth_img = Image.open(cloth_path)

    engine = get_engine(current_app.config.get('TRYON_ENGINE', 'mediapipe'))
    result = engine.composite(user_photo, cloth_img, clothing.display_category())

    result_filename = f"result_{active_photo.filename}"
    result_dir = os.path.join(current_app.config['RESULT_FOLDER'], str(current_user.id))
    os.makedirs(result_dir, exist_ok=True)
    result_path = os.path.join(result_dir, result_filename)
    result.save(result_path)

    # 传递结果给模板
    return redirect(url_for('main.index', result=f'{current_user.id}/{result_filename}'))
```

- [ ] **Step 7: 在 app.py 注册 tryon blueprint 并修改 main index 接受 result 参数**

```python
from blueprints.tryon import tryon_bp
app.register_blueprint(tryon_bp)
```

- [ ] **Step 8: 修改 blueprints/main.py 的 index 路由传递 result 参数**

替换 `index()` 函数的返回语句为：

```python
result_filename = request.args.get('result')
return render_template('index.html', photos=photos, active_photo=active_photo, result_filename=result_filename)
```

- [ ] **Step 9: 运行试穿测试**

```bash
source venv/Scripts/activate && python -m pytest tests/test_tryon.py -v
```

Expected: 3 tests PASS

---

### Task 9: 前端 — 公共布局和认证页面

**Files:**
- Create: `templates/base.html`
- Rewrite: `templates/login.html`, `templates/register.html`, `templates/reset_password.html`

- [ ] **Step 1: 创建 templates/base.html（带完整设计系统）**

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}FitAI{% endblock %} · 智能试衣</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #F7F4F0;
      --surface: #FFFFFF;
      --surface-2: #F0EDE8;
      --border: #E5E0D9;
      --text-primary: #1C1A17;
      --text-secondary: #7A7267;
      --accent: #C8733A;
      --accent-light: #F2E6DB;
      --accent-hover: #A85E2C;
      --success: #4A8C6F;
      --danger: #C84040;
      --shadow-sm: 0 2px 8px rgba(28,26,23,.06);
      --shadow-md: 0 8px 32px rgba(28,26,23,.10);
      --radius: 20px;
      --radius-sm: 12px;
      --transition: 0.35s cubic-bezier(.4,0,.2,1);
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'DM Sans', sans-serif;
      background: var(--bg);
      color: var(--text-primary);
      min-height: 100vh;
    }
    .nav {
      position: sticky; top: 0; z-index: 100;
      display: flex; align-items: center; justify-content: space-between;
      padding: 18px 48px;
      background: rgba(247,244,240,.88);
      backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border);
    }
    .nav-logo {
      font-family: 'Playfair Display', serif;
      font-size: 1.25rem; font-weight: 600;
      color: var(--text-primary);
      text-decoration: none;
    }
    .nav-logo span { color: var(--accent); }
    .nav-links { display: flex; gap: 24px; align-items: center; }
    .nav-links a, .nav-user-btn {
      font-size: .85rem; font-weight: 500;
      color: var(--text-secondary); text-decoration: none;
      padding: 6px 12px; border-radius: 8px;
      transition: var(--transition);
    }
    .nav-links a:hover, .nav-links a.active { color: var(--accent); background: var(--accent-light); }
    .nav-user-menu {
      position: relative; display: inline-block;
    }
    .nav-user-menu .dropdown {
      display: none; position: absolute; right: 0; top: 100%;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      box-shadow: var(--shadow-md);
      min-width: 160px;
      padding: 8px;
    }
    .nav-user-menu:hover .dropdown { display: block; }
    .dropdown a, .dropdown button {
      display: block; width: 100%; text-align: left;
      padding: 8px 12px; border-radius: 8px;
      font-size: .82rem; color: var(--text-primary);
      text-decoration: none; background: none; border: none;
      cursor: pointer; font-family: inherit;
    }
    .dropdown a:hover, .dropdown button:hover { background: var(--surface-2); color: var(--accent); }
    .dropdown .divider { height: 1px; background: var(--border); margin: 6px 0; }

    .flash-messages { max-width: 600px; margin: 24px auto 0; padding: 0 24px; }
    .flash { padding: 12px 16px; border-radius: var(--radius-sm); margin-bottom: 8px; font-size: .85rem; }
    .flash.success { background: rgba(74,140,111,.1); border: 1px solid rgba(74,140,111,.2); color: var(--success); }
    .flash.error { background: rgba(200,64,64,.08); border: 1px solid rgba(200,64,64,.2); color: var(--danger); }
    .flash.info { background: var(--surface-2); border: 1px solid var(--border); color: var(--text-secondary); }

    .auth-page { display: flex; align-items: center; justify-content: center; min-height: 80vh; padding: 24px; }
    .auth-card {
      background: var(--surface); border: 1px solid var(--border);
      border-radius: var(--radius); padding: 40px;
      box-shadow: var(--shadow-sm); width: 100%; max-width: 420px;
    }
    .auth-card h1 {
      font-family: 'Playfair Display', serif; font-size: 1.8rem;
      font-weight: 600; margin-bottom: 24px; text-align: center;
    }
    .form-group { margin-bottom: 16px; }
    .form-group label { display: block; font-size: .8rem; font-weight: 500; color: var(--text-secondary); margin-bottom: 6px; }
    .form-group input, .form-group select {
      width: 100%; padding: 12px 14px;
      border: 1.5px solid var(--border); border-radius: var(--radius-sm);
      font-family: 'DM Sans', sans-serif; font-size: .9rem;
      background: var(--bg); transition: border-color var(--transition);
    }
    .form-group input:focus, .form-group select:focus { outline: none; border-color: var(--accent); }
    .btn {
      display: inline-flex; align-items: center; justify-content: center; gap: 8px;
      font-family: 'DM Sans', sans-serif; font-size: .9rem; font-weight: 500;
      padding: 12px 24px; border-radius: 99px; border: none; cursor: pointer;
      transition: var(--transition); text-decoration: none;
    }
    .btn-primary { background: var(--text-primary); color: var(--bg); width: 100%; }
    .btn-primary:hover { background: var(--accent); }
    .btn-accent { background: var(--accent); color: white; }
    .btn-accent:hover { background: var(--accent-hover); }
    .btn-outline { background: transparent; border: 1.5px solid var(--border); color: var(--text-primary); }
    .btn-outline:hover { border-color: var(--text-primary); }
    .btn-sm { font-size: .78rem; padding: 8px 14px; }
    .btn-danger { background: var(--danger); color: white; }
    .auth-links { text-align: center; margin-top: 20px; font-size: .85rem; color: var(--text-secondary); }
    .auth-links a { color: var(--accent); text-decoration: none; font-weight: 500; }
    .auth-links a:hover { text-decoration: underline; }

    .container { max-width: 1060px; margin: 0 auto; padding: 32px 24px; }
    .section-title {
      font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 600;
      margin-bottom: 24px;
    }
    .grid { display: grid; gap: 20px; }
    .grid-2 { grid-template-columns: 1fr 1fr; }
    .grid-3 { grid-template-columns: repeat(3, 1fr); }
    .grid-4 { grid-template-columns: repeat(4, 1fr); }
    .card {
      background: var(--surface); border: 1px solid var(--border);
      border-radius: var(--radius); padding: 24px; box-shadow: var(--shadow-sm);
    }
    .card-title { font-size: .7rem; font-weight: 500; letter-spacing: .1em; text-transform: uppercase; color: var(--text-secondary); margin-bottom: 16px; }

    .empty-state { text-align: center; padding: 60px 20px; color: var(--text-secondary); }
    .empty-state-icon { width: 56px; height: 56px; margin: 0 auto 16px; background: var(--surface-2); border-radius: 14px; display: flex; align-items: center; justify-content: center; }

    @media (max-width: 720px) {
      .nav { padding: 16px 20px; }
      .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
    }
  </style>
  {% block head %}{% endblock %}
</head>
<body>
  <nav class="nav">
    <a href="{{ url_for('main.index') }}" class="nav-logo">Fit<span>AI</span></a>
    <div class="nav-links">
      {% if current_user.is_authenticated %}
        <a href="{{ url_for('main.index') }}" class="{% if request.endpoint == 'main.index' %}active{% endif %}">试穿</a>
        <a href="{{ url_for('wardrobe.index') }}" class="{% if request.endpoint and request.endpoint.startswith('wardrobe') %}active{% endif %}">衣橱</a>
        <div class="nav-user-menu">
          <span class="nav-user-btn">{{ current_user.username }} ▾</span>
          <div class="dropdown">
            <a href="{{ url_for('main.index') }}">我的照片</a>
            <div class="divider"></div>
            <a href="{{ url_for('auth.logout') }}">退出登录</a>
          </div>
        </div>
      {% else %}
        <a href="{{ url_for('auth.login') }}">登录</a>
        <a href="{{ url_for('auth.register') }}">注册</a>
      {% endif %}
    </div>
  </nav>

  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      <div class="flash-messages">
        {% for category, message in messages %}
          <div class="flash {{ category }}">{{ message }}</div>
        {% endfor %}
      </div>
    {% endif %}
  {% endwith %}

  {% block content %}{% endblock %}

  <footer style="text-align:center; padding:32px 24px; border-top:1px solid var(--border); font-size:.78rem; color:var(--text-secondary); margin-top:60px;">
    FitAI · 虚拟试衣系统 &nbsp;|&nbsp; Powered by <span style="color:var(--accent);">PyTorch × Flask</span> &nbsp;|&nbsp; 武汉大学
  </footer>
</body>
</html>
```

- [ ] **Step 2: 更新 templates/login.html**

```html
{% extends "base.html" %}
{% block title %}登录{% endblock %}
{% block content %}
<div class="auth-page">
  <div class="auth-card">
    <h1>欢迎回来</h1>
    <form method="post">
      <div class="form-group">
        <label>邮箱</label>
        <input type="email" name="email" placeholder="your@email.com" required>
      </div>
      <div class="form-group">
        <label>密码</label>
        <input type="password" name="password" placeholder="输入密码" required>
      </div>
      <button type="submit" class="btn btn-primary">登录</button>
    </form>
    <div class="auth-links">
      <p>没有账号？<a href="{{ url_for('auth.register') }}">立即注册</a></p>
      <p><a href="{{ url_for('auth.reset_password') }}">忘记密码？</a></p>
    </div>
  </div>
</div>
{% endblock %}
```

- [ ] **Step 3: 更新 templates/register.html**

```html
{% extends "base.html" %}
{% block title %}注册{% endblock %}
{% block content %}
<div class="auth-page">
  <div class="auth-card">
    <h1>创建账号</h1>
    <form method="post">
      <div class="form-group">
        <label>用户名</label>
        <input type="text" name="username" placeholder="2-20个字符" required minlength="2">
      </div>
      <div class="form-group">
        <label>邮箱</label>
        <input type="email" name="email" placeholder="your@email.com" required>
      </div>
      <div class="form-group">
        <label>密码</label>
        <input type="password" name="password" placeholder="至少6位" required minlength="6">
      </div>
      <div class="form-group">
        <label>确认密码</label>
        <input type="password" name="confirm_password" placeholder="再次输入密码" required>
      </div>
      <button type="submit" class="btn btn-primary">注册</button>
    </form>
    <div class="auth-links">
      <p>已有账号？<a href="{{ url_for('auth.login') }}">立即登录</a></p>
    </div>
  </div>
</div>
{% endblock %}
```

- [ ] **Step 4: 更新 templates/reset_password.html**

```html
{% extends "base.html" %}
{% block title %}重置密码{% endblock %}
{% block content %}
<div class="auth-page">
  <div class="auth-card">
    <h1>重置密码</h1>
    {% if token %}
      <form method="post">
        <input type="hidden" name="token" value="{{ token }}">
        <div class="form-group">
          <label>新密码</label>
          <input type="password" name="password" placeholder="至少6位" required minlength="6">
        </div>
        <div class="form-group">
          <label>确认新密码</label>
          <input type="password" name="confirm_password" placeholder="再次输入" required>
        </div>
        <button type="submit" class="btn btn-primary">重置密码</button>
      </form>
    {% else %}
      <form method="post">
        <div class="form-group">
          <label>注册邮箱</label>
          <input type="email" name="email" placeholder="输入注册时使用的邮箱" required>
        </div>
        <button type="submit" class="btn btn-primary">发送重置链接</button>
      </form>
    {% endif %}
    <div class="auth-links">
      <p><a href="{{ url_for('auth.login') }}">返回登录</a></p>
    </div>
  </div>
</div>
{% endblock %}
```

- [ ] **Step 5: 验证认证流程可用**

```bash
source venv/Scripts/activate && python app.py &
sleep 2
curl -s http://localhost:5000/register | head -20
```

Expected: 返回注册页面 HTML，包含 "创建账号" 标题。

---

### Task 10: 前端 — 试穿主页 index.html

**Files:**
- Rewrite: `templates/index.html`

- [ ] **Step 1: 重写 templates/index.html（完整试穿界面）**

```html
{% extends "base.html" %}
{% block title %}试穿{% endblock %}
{% block content %}
<div class="hero" style="text-align:center; padding:40px 24px 20px;">
  <h1 style="font-family:'Playfair Display',serif;font-size:2.2rem;font-weight:600;">智能虚拟试穿</h1>
  <p style="color:var(--text-secondary);max-width:460px;margin:8px auto 0;">上传你的照片和衣物，AI 自动识别分类并模拟试穿效果</p>
</div>

<div class="container">
  <div class="grid grid-2">

    <!-- 左侧：照片和衣物选择 -->
    <div>
      <!-- 个人照片区 -->
      <div class="card" style="margin-bottom:20px;">
        <div class="card-title">我的试穿照片</div>
        {% if photos %}
          <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px;">
            {% for photo in photos %}
              <div style="position:relative;width:80px;height:80px;border-radius:10px;overflow:hidden;border:2px solid {% if photo.is_active %}var(--accent){% else %}var(--border){% endif %};">
                <img src="{{ url_for('static', filename='uploads/' + current_user.id|string + '/' + photo.filename) }}" style="width:100%;height:100%;object-fit:cover;">
                {% if not photo.is_active %}
                <form method="post" action="{{ url_for('main.set_active_photo', photo_id=photo.id) }}" style="position:absolute;inset:0;">
                  <button type="submit" style="width:100%;height:100%;background:transparent;border:none;cursor:pointer;opacity:50%;" title="设为当前"></button>
                </form>
                {% endif %}
              </div>
            {% endfor %}
          </div>
        {% else %}
          <div class="empty-state" style="padding:24px;">
            <p style="font-size:.85rem;">还没有上传照片</p>
          </div>
        {% endif %}
        <form method="post" action="{{ url_for('main.upload_photo') }}" enctype="multipart/form-data">
          <div style="display:flex;gap:8px;">
            <input type="file" name="photo" accept="image/*" required style="flex:1;font-size:.82rem;">
            <button type="submit" class="btn btn-accent btn-sm">上传照片</button>
          </div>
        </form>
        {% if active_photo %}<p style="font-size:.75rem;color:var(--accent);margin-top:6px;">✓ 当前试穿底图已就绪</p>{% endif %}
      </div>

      <!-- 衣物选择区 -->
      <div class="card">
        <div class="card-title">选择衣物</div>
        <div id="clothing-selector" style="display:flex;gap:10px;flex-wrap:wrap;max-height:200px;overflow-y:auto;margin-bottom:16px;">
          <p style="font-size:.82rem;color:var(--text-secondary);">加载中...</p>
        </div>
        <form method="post" id="tryon-form" style="display:none;">
          <button type="submit" class="btn btn-accent" style="width:100%;">立即试衣</button>
        </form>
        <p style="text-align:center;font-size:.8rem;color:var(--text-secondary);margin-top:8px;">
          在<a href="{{ url_for('wardrobe.index') }}" style="color:var(--accent);">衣橱</a>中上传更多衣物
        </p>
      </div>
    </div>

    <!-- 右侧：试穿结果 -->
    <div>
      <div class="card">
        <div class="card-title">试穿效果</div>
        {% if result_filename %}
          <div style="border-radius:var(--radius-sm);overflow:hidden;border:1px solid var(--border);">
            <img src="{{ url_for('static', filename='results/' + result_filename) }}" style="width:100%;" alt="试穿效果">
          </div>
        {% else %}
          <div class="empty-state">
            <div class="empty-state-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" stroke="var(--text-secondary)" stroke-width="1.8" stroke-linecap="round"/>
              </svg>
            </div>
            <p>选择衣物后点击试衣<br>效果将显示在这里</p>
          </div>
        {% endif %}
      </div>
    </div>

  </div>
</div>
{% endblock %}

{% block head %}
<script>
// 加载衣橱衣物列表
document.addEventListener('DOMContentLoaded', () => {
  fetch('/api/wardrobe-items')
    .then(r => r.json())
    .then(items => {
      const container = document.getElementById('clothing-selector');
      const form = document.getElementById('tryon-form');
      if (items.length === 0) {
        container.innerHTML = '<p style="font-size:.82rem;color:var(--text-secondary);">衣橱为空，请先上传衣物</p>';
        return;
      }
      container.innerHTML = '';
      items.forEach(item => {
        const div = document.createElement('div');
        div.style.cssText = 'width:72px;height:72px;border-radius:10px;overflow:hidden;border:2px solid var(--border);cursor:pointer;position:relative;';
        div.innerHTML = `<img src="/static/uploads/${item.user_id}/${item.filename}" style="width:100%;height:100%;object-fit:cover;">
          <span style="position:absolute;bottom:2px;left:2px;right:2px;font-size:.55rem;background:rgba(0,0,0,.6);color:white;padding:1px 4px;border-radius:4px;text-align:center;">${item.display_category}</span>`;
        div.addEventListener('click', () => {
          document.querySelectorAll('#clothing-selector > div').forEach(d => d.style.borderColor = 'var(--border)');
          div.style.borderColor = 'var(--accent)';
          form.style.display = 'block';
          form.action = `/tryon/${item.id}`;
        });
        container.appendChild(div);
      });
    });
});
</script>
{% endblock %}
```

- [ ] **Step 2: 创建衣橱 API 端点（在 wardrobe blueprint 中）**

向 `blueprints/wardrobe.py` 追加：

```python
@wardrobe_bp.route('/api/wardrobe-items')
@login_required
def api_items():
    """返回当前用户的衣橱物品 JSON（供前端 AJAX 加载）"""
    items = Clothing.query.filter_by(user_id=current_user.id).order_by(Clothing.uploaded_at.desc()).all()
    return {
        'items': [{
            'id': i.id,
            'filename': i.filename,
            'category': i.category,
            'manual_category': i.manual_category,
            'display_category': i.display_category(),
            'user_id': i.user_id
        } for i in items]
    }
```

注意：此 API 需要注册为 `/api/wardrobe-items`（在 wardrobe blueprint 的 `url_prefix` 下），所以实际路径为 `/wardrobe/api/wardrobe-items`。前端 fetch 路径需要对应修改。

- [ ] **Step 3: 修正前端 fetch URL**

将 `index.html` 中的 `fetch('/api/wardrobe-items')` 改为 `fetch('/wardrobe/api/wardrobe-items')`。

- [ ] **Step 4: 验证试穿主页可访问**

```bash
source venv/Scripts/activate && python -m pytest tests/test_photo.py -v
```

Expected: 所有测试仍然通过。

---

### Task 11: 前端 — 衣橱管理页面

**Files:**
- Create: `templates/wardrobe.html`

- [ ] **Step 1: 创建 templates/wardrobe.html**

```html
{% extends "base.html" %}
{% block title %}衣橱{% endblock %}
{% block content %}
<div class="container">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;">
    <h1 class="section-title" style="margin-bottom:0;">我的衣橱</h1>
    <form method="post" action="{{ url_for('wardrobe.upload') }}" enctype="multipart/form-data" style="display:flex;gap:8px;">
      <input type="file" name="clothing" accept="image/*" required style="font-size:.82rem;">
      <button type="submit" class="btn btn-accent btn-sm">上传衣物</button>
    </form>
  </div>

  {% if items %}
    <div class="grid grid-4">
      {% for item in items %}
        <div class="card" style="padding:16px;text-align:center;">
          <div style="width:100%;aspect-ratio:1;border-radius:var(--radius-sm);overflow:hidden;background:var(--bg);margin-bottom:12px;">
            <img src="{{ url_for('static', filename='uploads/' + current_user.id|string + '/' + item.filename) }}" style="width:100%;height:100%;object-fit:cover;">
          </div>
          <p style="font-size:.78rem;font-weight:500;margin-bottom:4px;">AI 识别: <span style="color:var(--accent);">{{ item.category }}</span></p>
          {% if item.manual_category %}
            <p style="font-size:.72rem;color:var(--success);margin-bottom:4px;">用户修正: {{ item.manual_category }}</p>
          {% endif %}
          <form method="post" action="{{ url_for('wardrobe.edit', item_id=item.id) }}" style="display:flex;gap:6px;margin-bottom:6px;">
            <select name="manual_category" style="flex:1;font-size:.72rem;padding:6px;border:1px solid var(--border);border-radius:6px;background:var(--bg);">
              <option value="">— 自动识别 —</option>
              {% for cls in classes %}
                <option value="{{ cls }}" {% if item.manual_category == cls %}selected{% endif %}>{{ cls }}</option>
              {% endfor %}
            </select>
            <button type="submit" class="btn btn-outline btn-sm">修正</button>
          </form>
          <form method="post" action="{{ url_for('wardrobe.delete', item_id=item.id) }}" onsubmit="return confirm('确定删除这件衣物？');">
            <button type="submit" class="btn btn-danger btn-sm" style="width:100%;">删除</button>
          </form>
        </div>
      {% endfor %}
    </div>
  {% else %}
    <div class="empty-state">
      <div class="empty-state-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V7M3 7l9 6 9-6" stroke="var(--text-secondary)" stroke-width="1.8" stroke-linecap="round"/>
        </svg>
      </div>
      <p>衣橱还是空的<br>上传你的第一件衣物吧</p>
    </div>
  {% endif %}
</div>
{% endblock %}
```

- [ ] **Step 2: 验证衣橱页面可访问**

```bash
source venv/Scripts/activate && python -m pytest tests/test_wardrobe.py::TestWardrobe::test_wardrobe_page -v
```

Expected: PASS

---

### Task 12: 安全加固 + 最终集成

**Files:**
- Modify: `app.py` (CSRF, security headers)
- Modify: `blueprints/auth.py` (CSRF token 到模板)

- [ ] **Step 1: 在 config.py 添加安全配置**

```python
class Config:
    # ... 已有配置 ...
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
```

- [ ] **Step 2: 在 app.py 添加 CSRF 保护**

Flask-WTF 的 CSRF 需要表单中有 `csrf_token`。由于我们用的是原生 HTML 表单而非 WTForms，使用 Flask-WTF 的 `CSRFProtect` 并在模板中手动渲染 token：

```python
# app.py — create_app 函数中添加
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()
csrf.init_app(app)
```

- [ ] **Step 3: 在所有 POST 表单中添加 CSRF token**

在 `base.html` 的 `<body>` 最前加入全局 JS，自动给 POST 表单注入 token：

```html
<meta name="csrf-token" content="{{ csrf_token() }}">
<script>
// 自动为所有 POST 表单添加 CSRF token
document.addEventListener('DOMContentLoaded', () => {
  const token = document.querySelector('meta[name="csrf-token"]').content;
  document.querySelectorAll('form[method="post"]').forEach(form => {
    if (!form.querySelector('input[name="csrf_token"]')) {
      const input = document.createElement('input');
      input.type = 'hidden';
      input.name = 'csrf_token';
      input.value = token;
      form.appendChild(input);
    }
  });
});
</script>
```

- [ ] **Step 4: 在 auth.py 中针对测试环境禁用 CSRF 的处理**

修改 `blueprints/auth.py`，确保表单提交在测试模式下正常工作。测试 config `TestConfig` 已设置 `WTF_CSRF_ENABLED = False`。

- [ ] **Step 5: 运行全部测试**

```bash
source venv/Scripts/activate && python -m pytest tests/ -v
```

Expected: 全部测试 PASS（约 29 个测试）。

- [ ] **Step 6: 验证完整流程**

```bash
source venv/Scripts/activate && python app.py
```

手动测试：
1. 访问 http://localhost:5000 → 重定向到登录页
2. 点击注册 → 填写表单 → 提交 → 查看控制台验证链接
3. 点击验证链接 → 邮箱验证成功
4. 登录 → 进入试穿主页
5. 上传个人照片
6. 导航到衣橱 → 上传衣物 → 看到 AI 分类结果
7. 返回试穿页 → 选择衣物 → 点击试衣 → 查看结果
8. 登出

---

### 任务依赖图

```
Task 1 (基础设施)
  └─ Task 2 (数据模型)
       └─ Task 3 (注册)
            └─ Task 4 (登录/退出)
                 └─ Task 5 (邮箱验证+密码重置)
       └─ Task 6 (照片管理) [依赖 Task 4]
       └─ Task 7 (衣橱 CRUD) [依赖 Task 4]
            └─ Task 8 (试穿引擎) [依赖 Task 6, 7]
       └─ Task 9 (认证页面)
       └─ Task 10 (试穿主页) [依赖 Task 6, 7]
       └─ Task 11 (衣橱页面) [依赖 Task 7]
Task 12 (安全加固) [依赖全部]
```
