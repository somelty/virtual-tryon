'''
虚拟试衣系统的Web应用服务端程序
2025.03: Created by Xu Xiaoyang, Zhang Hua
2025.05: Modified by Zhang Hua
  - 把模型类 FashionCNN 的定义提取出来，放到 model.py 中
  - 语法适配 PyTorch 2.x
  - 在 Windows 11 的 Python 3.12.x 、 PyTorch 2.7 和 Flask 3.1.0 中测试通过
'''
# 导入 Flask 框架及其模板渲染、请求、重定向、URL 生成模块
from flask import Flask, render_template, request

# 导入操作系统、PyTorch、神经网络模块、常用函数模块、图像处理库（PIL）
import os
import torch
# import torch.nn as nn
from torchvision import transforms
from PIL import Image

# 导入自定义的神经网络模型类
from model import FashionCNN


# 创建 Flask 应用实例
app = Flask(__name__)

# 配置上传和结果目录，如果目录不存在则自动创建
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULT_FOLDER'] = 'static/results'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

# 加载预训练模型状态字典
model = FashionCNN()
model.load_state_dict(torch.load('./cnn_model.pth'))
model.eval()  # 切换为评估模式

# 图像预处理流程
preprocess = transforms.Compose([
    transforms.Grayscale(),  # 转为灰度
    transforms.Resize((28, 28)),  # 缩放到28x28
    transforms.ToTensor(),  # 转为张量
    transforms.Normalize((0.5,), (0.5,))  # 标准化
])

# 类别标签
classes = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
           'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# 预定义衣物粘贴在假人图片上的区域
region_mapping = {
    'T-shirt/top': (220, 150, 380, 330),
    'Pullover': (220, 150, 380, 330),
    'Dress': (210, 150, 390, 600),
    'Coat': (220, 150, 380, 360),
    'Shirt': (220, 150, 380, 330),
    'Trouser': (240, 330, 360, 680),
    'Sandal': [(250, 680, 280, 720), (320, 680, 350, 720)],
    'Sneaker': [(250, 680, 280, 720), (320, 680, 350, 720)],
    'Ankle boot': [(250, 680, 280, 720), (320, 680, 350, 720)],
    'Bag': (140, 280, 220, 400)
}

# 根据目标区域调整上传图片的大小


def fit_to_region(image, region):
    target_width = region[2] - region[0]
    target_height = region[3] - region[1]
    return image.resize((target_width, target_height))

# 主页面路由


@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_label = None
    result_filename = None
    if request.method == 'POST':
        file = request.files['file']
        if file.filename != '' and file:
            # 保存上传文件
            upload_path = os.path.join(
                app.config['UPLOAD_FOLDER'], file.filename)
            file.save(upload_path)

            # 读取上传图片并预测分类
            clothing_image = Image.open(upload_path)
            input_tensor = preprocess(clothing_image).unsqueeze(0)

            # 使用推理模式（PyTorch 2.x优化）
            with torch.inference_mode():
                outputs = model(input_tensor)
                predicted = torch.argmax(outputs, dim=1)

            predicted_label = classes[predicted.item()]

            # 打开假人图片作为底图
            mannequin_path = 'static/mannequin.png'
            mannequin = Image.open(mannequin_path).convert("RGBA")
            overlay = Image.open(upload_path).convert("RGBA")

            # 给上传图片增加透明度
            overlay.putalpha(230)

            # 根据预测结果将衣物图片粘贴到假人相应位置
            composite = mannequin.copy()
            region = region_mapping.get(predicted_label)
            if region:
                if isinstance(region, list):  # 如果是鞋子（有多个位置）
                    for r in region:
                        fitted_overlay = fit_to_region(overlay, r)
                        composite.paste(fitted_overlay, r[:2], fitted_overlay)
                else:
                    fitted_overlay = fit_to_region(overlay, region)
                    composite.paste(fitted_overlay, region[:2], fitted_overlay)

            # 将合成后的图片保存
            result_filename = "result_" + file.filename
            result_path = os.path.join(
                app.config['RESULT_FOLDER'], result_filename)
            composite.save(result_path)

    # 渲染模板，并传递结果文件名和分类标签
    return render_template('index.html', predicted_label=predicted_label, result_filename=result_filename)


# 启动 Flask 应用
if __name__ == '__main__':
    app.run(debug=True)
