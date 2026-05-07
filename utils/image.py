import os
import uuid
from PIL import Image

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
