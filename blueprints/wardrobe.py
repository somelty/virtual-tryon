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

CLASSES = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
           'Sandal', 'Shirt', 'Sneaker', 'Ankle boot', 'Bag']

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
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'],
                           str(current_user.id), item.filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    db.session.delete(item)
    db.session.commit()
    flash('衣物已删除', 'info')
    return redirect(url_for('wardrobe.index'))
