import os
from flask import Blueprint, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from PIL import Image
from models import db
from models.clothing import Clothing
from models.photo import Photo
from engines import get_engine

# 虚拟试穿蓝图，url_prefix='/tryon' 使所有路由自动带有 /tryon 前缀
tryon_bp = Blueprint('tryon', __name__, url_prefix='/tryon')


@tryon_bp.route('/<int:clothing_id>', methods=['POST'])
@login_required
def try_on(clothing_id):
    """
    虚拟试穿核心流程：
    1. 校验衣物和激活照片是否存在
    2. 从磁盘加载人物照片和衣物图片
    3. 调用试穿引擎合成效果图
    4. 保存结果并重定向到首页展示
    """
    # 校验衣物归属，防止越权访问他人衣物
    clothing = Clothing.query.filter_by(id=clothing_id, user_id=current_user.id).first()
    if not clothing:
        abort(404)

    # 必须有激活的照片作为试穿底图
    active_photo = Photo.query.filter_by(user_id=current_user.id, is_active=True).first()
    if not active_photo:
        flash('请先上传个人照片并设为当前试穿底图', 'error')
        return redirect(url_for('main.index'))

    # 构建人物照片和衣物图片的磁盘路径（按用户 ID 分子目录存储）
    user_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], str(current_user.id))
    photo_path = os.path.join(user_dir, active_photo.filename)
    cloth_path = os.path.join(user_dir, clothing.filename)

    # 加载图片到内存
    user_photo = Image.open(photo_path)
    cloth_img = Image.open(cloth_path)

    # 获取试穿引擎（默认 mediapipe），调用 composite 完成合成
    engine = get_engine(current_app.config.get('TRYON_ENGINE', 'mediapipe'))
    result = engine.composite(user_photo, cloth_img, clothing.display_category())

    # 结果文件命名以 result_ 为前缀，方便与原始照片区分
    result_filename = f"result_{active_photo.filename}"
    result_dir = os.path.join(current_app.config['RESULT_FOLDER'], str(current_user.id))
    os.makedirs(result_dir, exist_ok=True)
    result_path = os.path.join(result_dir, result_filename)

    # RGBA 模式无法直接存为 JPEG，需转为 RGB
    if result.mode == 'RGBA':
        result = result.convert('RGB')
    result.save(result_path)

    # 通过查询参数将结果路径传给首页，前端据此展示效果图
    return redirect(url_for('main.index', result=f'{current_user.id}/{result_filename}'))