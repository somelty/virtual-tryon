from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from models import db
from models.photo import Photo
from utils.image import validate_image, save_upload

# 主页蓝图，挂载首页展示、照片上传/切换/删除等核心业务路由
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def index():
    """首页：展示当前用户的所有照片、当前激活的试穿照片、处理结果"""
    # 按上传时间倒序获取用户的全部照片
    photos = Photo.query.filter_by(user_id=current_user.id).order_by(Photo.uploaded_at.desc()).all()
    # 获取当前被选为"试穿基准"的那张照片（每个用户最多一张）
    active_photo = Photo.query.filter_by(user_id=current_user.id, is_active=True).first()
    # result 参数由处理完成后重定向传入，用于前端展示生成的效果图
    result_filename = request.args.get('result')
    return render_template('index.html', photos=photos, active_photo=active_photo, result_filename=result_filename)


@main_bp.route('/upload-photo', methods=['POST'])
@login_required
def upload_photo():
    """照片上传：支持多文件，校验 → 存储 → 写入数据库（首张上传自动设为激活）"""
    files = request.files.getlist('photos')
    if not files or all(f.filename == '' for f in files):
        flash('未选择文件', 'error')
        return redirect(url_for('main.index'))

    existing_active = Photo.query.filter_by(user_id=current_user.id, is_active=True).first()
    uploaded = 0
    for file in files:
        valid, msg = validate_image(file)
        if not valid:
            flash(f'{file.filename}: {msg}', 'error')
            continue
        filename = save_upload(file, current_app.config['UPLOAD_FOLDER'],
                               subfolder=str(current_user.id))
        photo = Photo(user_id=current_user.id, filename=filename)
        if not existing_active and uploaded == 0:
            photo.is_active = True
        db.session.add(photo)
        uploaded += 1

    if uploaded:
        db.session.commit()
        flash(f'{uploaded} 张照片上传成功', 'success')
    return redirect(url_for('main.index'))


@main_bp.route('/set-photo/<int:photo_id>', methods=['POST'])
@login_required
def set_active_photo(photo_id):
    """切换试穿基准照片：将指定照片设为激活，取消其他照片的激活状态"""
    # set_active 为模型层封装的原子操作：先取消该用户所有激活，再激活目标照片
    success = Photo.set_active(current_user.id, photo_id)
    if not success:
        abort(404)
    flash('已切换试穿照片', 'success')
    return redirect(url_for('main.index'))


@main_bp.route('/delete-photo/<int:photo_id>', methods=['POST'])
@login_required
def delete_photo(photo_id):
    """删除照片：如果删除的是激活照片，自动将最新上传的照片设为激活"""
    # 限定 user_id，防止越权删除他人照片
    photo = Photo.query.filter_by(id=photo_id, user_id=current_user.id).first()
    if not photo:
        abort(404)

    was_active = photo.is_active
    db.session.delete(photo)
    db.session.commit()

    # 如果删除的是当前激活照片，自动将剩余照片中最新的那张设为激活
    if was_active:
        latest = Photo.query.filter_by(user_id=current_user.id).order_by(Photo.uploaded_at.desc()).first()
        if latest:
            latest.is_active = True
            db.session.commit()

    flash('照片已删除', 'info')
    return redirect(url_for('main.index'))