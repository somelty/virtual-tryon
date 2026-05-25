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

# 衣橱蓝图，url_prefix 使所有路由自动带有 /wardrobe 前缀
wardrobe_bp = Blueprint('wardrobe', __name__, url_prefix='/wardrobe')

# Fashion-MNIST 的 10 个类别（与训练时标签顺序一致）
CLASSES = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
           'Sandal', 'Shirt', 'Sneaker', 'Ankle boot', 'Bag']

# CNN 模型单例，首次调用时加载，避免每次请求重复初始化
CNN_MODEL = None
# 预处理流水线：灰度化 → 缩放到 28x28（Fashion-MNIST 输入尺寸）→ 转张量 → 归一化
CNN_PREPROCESS = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])


def _get_cnn_model():
    """懒加载 CNN 模型，全局单例避免重复加载"""
    global CNN_MODEL
    if CNN_MODEL is None:
        CNN_MODEL = FashionCNN()
        # weights_only=True 防止 torch.load 的反序列化安全问题
        CNN_MODEL.load_state_dict(torch.load('./cnn_model.pth',
                                             map_location=torch.device('cpu'),
                                             weights_only=True))
        CNN_MODEL.eval()  # 切换到评估模式，关闭 dropout/batchnorm 训练行为
    return CNN_MODEL


def _classify_image(filepath):
    """对磁盘上的图片运行 CNN 分类，返回预测类别名"""
    model = _get_cnn_model()
    img = Image.open(filepath)
    # unsqueeze(0) 在第 0 维增加 batch 维度，将 (C,H,W) 变为 (1,C,H,W)
    tensor = CNN_PREPROCESS(img).unsqueeze(0)
    with torch.inference_mode():  # 推理模式，禁用梯度计算，减少内存占用
        outputs = model(tensor)
        predicted = torch.argmax(outputs, dim=1)
    return CLASSES[predicted.item()]


@wardrobe_bp.route('')
@login_required
def index():
    """衣橱首页：展示当前用户所有衣物及分类列表"""
    items = Clothing.query.filter_by(user_id=current_user.id).order_by(
        Clothing.uploaded_at.desc()).all()
    return render_template('wardrobe.html', items=items, classes=CLASSES)


@wardrobe_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    """衣物上传：支持多文件，校验 → 存储 → CNN 自动分类 → 写入数据库"""
    files = request.files.getlist('clothing')
    if not files or all(f.filename == '' for f in files):
        flash('未选择文件', 'error')
        return redirect(url_for('wardrobe.index'))

    uploaded = 0
    for file in files:
        valid, msg = validate_image(file)
        if not valid:
            flash(f'{file.filename}: {msg}', 'error')
            continue

        filename = save_upload(file, current_app.config['UPLOAD_FOLDER'],
                               subfolder=str(current_user.id))
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'],
                                str(current_user.id), filename)
        category = _classify_image(filepath)

        item = Clothing(user_id=current_user.id,
                        filename=filename, category=category)
        db.session.add(item)
        uploaded += 1

    if uploaded:
        db.session.commit()
        flash(f'{uploaded} 件衣物上传成功', 'success')
    return redirect(url_for('wardrobe.index'))


@wardrobe_bp.route('/<int:item_id>/edit', methods=['POST'])
@login_required
def edit(item_id):
    """手动修正衣物分类：当 CNN 识别不准时，用户可覆盖分类结果"""
    # user_id 过滤防越权
    item = Clothing.query.filter_by(
        id=item_id, user_id=current_user.id).first()
    if not item:
        abort(404)
    # manual_category 为空字符串时存 None，表示未手动覆盖
    item.manual_category = request.form.get(
        'manual_category', '').strip() or None
    db.session.commit()
    flash('分类已更新', 'success')
    return redirect(url_for('wardrobe.index'))


@wardrobe_bp.route('/<int:item_id>/delete', methods=['POST'])
@login_required
def delete(item_id):
    """删除衣物：同时删除数据库记录和磁盘文件"""
    item = Clothing.query.filter_by(
        id=item_id, user_id=current_user.id).first()
    if not item:
        abort(404)

    # 删除磁盘上的图片文件
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'],
                            str(current_user.id), item.filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    db.session.delete(item)
    db.session.commit()
    flash('衣物已删除', 'info')
    return redirect(url_for('wardrobe.index'))


@wardrobe_bp.route('/api/wardrobe-items')
@login_required
def api_items():
    """返回当前用户衣橱的 JSON 数据，供前端 AJAX 动态加载"""
    items = Clothing.query.filter_by(user_id=current_user.id).order_by(
        Clothing.uploaded_at.desc()).all()
    return {
        'items': [{
            'id': i.id,
            'filename': i.filename,
            'category': i.category,              # CNN 自动分类结果
            'manual_category': i.manual_category,  # 用户手动修正的分类
            'display_category': i.display_category(),  # 实际展示的分类（手动优先）
            'user_id': i.user_id
        } for i in items]
    }
