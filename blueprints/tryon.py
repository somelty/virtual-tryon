import os
from flask import Blueprint, redirect, url_for, flash, abort, current_app
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
    # RGBA 不能存为 JPEG，转为 RGB 或存为 PNG
    if result.mode == 'RGBA':
        result = result.convert('RGB')
    result.save(result_path)

    return redirect(url_for('main.index', result=f'{current_user.id}/{result_filename}'))
