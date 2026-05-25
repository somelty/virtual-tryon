from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db
from models.user import User
from utils.email import send_verification_email, send_reset_email

# 认证相关路由：注册、登录、退出、邮箱验证、密码重置
auth_bp = Blueprint('auth', __name__)


# 注册
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # 如果用户已登录，直接跳转到主页
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        # 提取表单数据，strip() 去除首尾空格, validate_image() 验证图片格式和大小，save_upload() 保存上传的图片并返回文件名
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # 验证输入数据的有效性，检查用户名长度、邮箱格式、密码长度和一致性，以及用户名和邮箱是否已被注册
        # 输入合法性检查，先做本地校验，减少不必要的数据库查询，提升性能和用户体验
        errors = []
        if not username or len(username) < 2:
            errors.append('用户名至少2个字符')
        if not email or '@' not in email:
            errors.append('请输入有效的邮箱')
        if len(password) < 6:
            errors.append('密码至少6个字符')
        if password != confirm_password:
            errors.append('两次密码不一致')

        # 唯一性检查 （查询数据库， 需要在本地校验之后）
        if User.query.filter_by(username=username).first():
            errors.append('用户名已被使用')
        if User.query.filter_by(email=email).first():
            errors.append('邮箱已被注册')

        # 有任意错误，则将错误信息通过 flash 传递给前端，并重新渲染注册页面，用户可以看到具体的错误提示并进行修改
        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('register.html')

        # 所有校验通过，创建用户对象，设置密码（加密存储），生成邮箱验证令牌，保存到数据库，并模拟发送验证邮件（在控制台输出验证链接）
        user = User(username=username, email=email)
        user.set_password(password)
        user.generate_verification_token()
        db.session.add(user)
        db.session.commit()

        # 模拟发送验证邮件，实际项目中应集成邮件服务，这里为了简化开发流程，直接在控制台输出验证链接，方便开发和测试
        print(
            f'\n[DEV] 邮箱验证链接: http://localhost:5000/verify/{user.verification_token}\n')
        flash('注册成功！验证邮件已发送（开发模式请查看控制台）', 'success')
        return redirect(url_for('auth.login'))

    # GET 请求直接渲染注册页面，用户可以在该页面填写注册信息并提交表单
    return render_template('register.html')

# 登录


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    '''用户登录：验证邮箱+密码，支持登录成功后跳转回来之前访问的页面'''
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        # 验证用户输入的邮箱和密码，查询数据库获取用户对象，检查密码是否正确，如果验证成功则登录用户，并根据 next 参数决定跳转到哪个页面（如果没有 next 参数，则默认跳转到主页）
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=True)  # remember=True 让用户在关闭浏览器后仍保持登录状态
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        # 不区分邮箱不存在和密码错误的情况，统一返回“邮箱或密码错误”，避免用户名枚举攻击
        flash('邮箱或密码错误', 'error')

    return render_template('login.html')


# 退出登录
@auth_bp.route('/logout')
@login_required
def logout():
    '''用户退出登录，调用 Flask-Login 的 logout_user() 函数清除用户会话，并重定向到登录页面'''
    logout_user()
    flash('已退出登录', 'info')
    return redirect(url_for('auth.login'))


# 验证
@auth_bp.route('/verify/<token>')
def verify_email(token):
    # 根据验证令牌查询用户，如果找到对应用户且令牌有效，则将用户的 email_verified 字段设置为 True，清除验证令牌，并保存到数据库。最后提示用户验证成功并重定向到登录页面。如果令牌无效或已过期，则提示错误信息并重定向到登录页面。
    user = User.query.filter_by(verification_token=token).first()
    if user:
        # 验证成功：标记邮箱已验证，清除验证令牌防止重复使用
        user.email_verified = True
        user.verification_token = None
        db.session.commit()
        flash('邮箱验证成功，请登录', 'success')
    else:
        # 验证失败：令牌无效或已过期，提示错误信息
        flash('验证链接无效或已过期', 'error')
    return redirect(url_for('auth.login'))


# 密码重置
@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    '''
    密码重置（两步流程）：                                                                                                                                                    
      - Step 1（无 token）：提交邮箱 → 生成 reset_token → 发送重置邮件                                                                                                          
      - Step 2（带 token）：通过邮件链接进入 → 提交新密码完成重置   
    '''
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    # token 可能来自 GET 请求的查询参数（用户点击邮件链接）或 POST 请求的表单数据（用户提交新密码），需要同时检查两种情况以支持完整的密码重置流程
    token = request.args.get('token') or request.form.get('token')

    if request.method == 'POST':
        if token:
            # Step 2 带 token 的 post：设置新密码，根据 reset_token 查询用户，验证令牌有效性（存在且未过期），如果有效则获取用户输入的新密码和确认密码，进行合法性检查（长度和一致性），如果检查通过则更新用户密码（加密存储），清除 reset_token 和过期时间，并提示用户密码重置成功，重定向到登录页面
            user = User.query.filter_by(reset_token=token).first()

            # 验证令牌有效性：用户存在且重置令牌未过期（reset_token_expiry 大于当前时间），如果无效则提示错误信息并重定向到密码重置请求页面
            if user and user.reset_token_expiry and user.reset_token_expiry > datetime.utcnow():
                password = request.form.get('password', '')
                confirm = request.form.get('confirm_password', '')
                if len(password) < 6:
                    flash('密码至少6个字符', 'error')
                elif password != confirm:
                    flash('两次密码不一致', 'error')
                else:
                    # 密码重置成功，更新密码并清除重置令牌和过期时间， 防止令牌被重复使用
                    user.set_password(password)
                    user.reset_token = None
                    user.reset_token_expiry = None
                    db.session.commit()
                    flash('密码已重置，请登录', 'success')
                    return redirect(url_for('auth.login'))
            else:
                # 。如果令牌无效或过期，则提示错误信息并重定向到密码重置请求页面。这种情况下用户需要重新提交邮箱来获取新的重置链接。
                flash('重置链接已过期', 'error')
                return redirect(url_for('auth.reset_password'))
        else:
            # Step 1: send reset email
            # 无 token 的 post：发送重置邮件
            email = request.form.get('email', '').strip()
            user = User.query.filter_by(email=email).first()
            if user:
                # 生成 token 和过期时间，保存到数据库，并模拟发送重置邮件（在控制台输出重置链接）
                t = user.generate_reset_token()
                db.session.commit()
                send_reset_email(user, t)
            # 无论用户是否存在，都提示“如果该邮箱已注册，重置邮件已发送”，以防止邮箱枚举攻击
            flash('如果该邮箱已注册，重置邮件已发送', 'info')
            return redirect(url_for('auth.login'))
    # GET 请求直接渲染密码重置页面，如果 URL 中包含 token，则将 token 传递给模板，用户可以在该页面输入新密码并提交表单完成密码重置流程
    return render_template('reset_password.html', token=token)
