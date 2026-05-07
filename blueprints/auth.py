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

        print(f'\n[DEV] 邮箱验证链接: http://localhost:5000/verify/{user.verification_token}\n')
        flash('注册成功！验证邮件已发送（开发模式请查看控制台）', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


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
