import os
import uuid
from PIL import Image, ImageOps

# 允许上传的图片格式白名单
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    """检查文件扩展名是否在白名单内"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_upload(file, upload_folder, subfolder=''):
    """保存上传文件，返回存储的文件名"""
    # 提取扩展名，生成 UUID 唯一文件名，防止路径遍历和文件名冲突
    ext = file.filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    dest_dir = os.path.join(upload_folder, subfolder)
    os.makedirs(dest_dir, exist_ok=True)
    filepath = os.path.join(dest_dir, unique_name)
    # 根据 EXIF Orientation 自动旋转图片（手机竖拍照片通常带旋转标记）
    img = Image.open(file)
    img = ImageOps.exif_transpose(img)
    # 统一转为 RGB 后保存，确保 JPEG 兼容性（RGBA 无法直接存为 JPEG）
    img = img.convert('RGB')
    img.save(filepath)
    return unique_name


def validate_image(file):
    """三层校验上传文件：非空、格式允许、PIL 可解析"""
    if not file or file.filename == '':
        return False, '未选择文件'
    if not allowed_file(file.filename):
        return False, '不支持的图片格式'
    try:
        img = Image.open(file)
        img.verify()  # PIL 校验图片完整性，不加载像素数据
        file.seek(0)  # verify() 消耗文件指针，需复位供后续读取
        return True, ''
    except Exception:
        return False, '无效的图片文件'
