from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
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
    result_filename = request.args.get('result')
    return render_template('index.html', photos=photos, active_photo=active_photo, result_filename=result_filename)


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
    if was_active:
        latest = Photo.query.filter_by(user_id=current_user.id).order_by(Photo.uploaded_at.desc()).first()
        if latest:
            latest.is_active = True
            db.session.commit()
    flash('照片已删除', 'info')
    return redirect(url_for('main.index'))
