'''
虚拟试衣系统的数据集样本展示程序
2025.03: Created by Xu Xiaoyang, Zhang Hua
2025.05: Modified by Zhang Hua
  - 语法适配 PyTorch 2.x
  - 在 Windows 11 的 Python 3.12.x 和 PyTorch 2.7 中测试通过
'''
# 导入必要的库
import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt


# 使用 transforms.ToTensor() 将图像转换为 Tensor
transform = transforms.ToTensor()
# 加载 Fashion MNIST 训练集
trainset = torchvision.datasets.FashionMNIST(
    root='./data',
    train=True,
    download=True,
    transform=transform
)

# 使用 DataLoader 将数据集划分为小批次（batch），便于后续训练或展示
trainloader = torch.utils.data.DataLoader(
    trainset,
    batch_size=64,
    shuffle=True
)

# 使用 DataLoader 将数据集划分为小批次（batch），便于后续训练或展示
classes = [
    'T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
    'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot'
]

# 使用iter()将DataLoader转换为迭代器，并调用next()获取第一个批次的数据
dataiter = iter(trainloader)
images, labels = next(dataiter)
# 只取前8个样本及其对应标签，用于展示
images8 = images[:8]
labels8 = labels[:8]

# 创建一个图像窗口，包含1行8列的子图，figsize 用于调整窗口大小
fig, axes = plt.subplots(1, 8, figsize=(15, 3))

# 遍历这8个子图，每个子图显示一张图像和对应的类别标签
for idx, ax in enumerate(axes):
    # 将单张图像从 Tensor 转换为 numpy 数组
    # 转换为CHW到HWC格式（PyTorch 2.x推荐使用.permute()）
    # squeeze() 用于去除单一通道的维度（例如将形状 [1, H, W] 转换为 [H, W]），方便显示灰度图
    img = images8[idx].permute(1, 2, 0).numpy().squeeze()
    # 使用 imshow() 显示灰度图像，并指定 cmap='gray' 显示为灰度图
    ax.imshow(img, cmap='gray')
    # 根据标签设置子图标题，classes[labels8[idx]] 获取对应的类别名称
    # fontsize 设置标题字体大小，pad 设置标题与图像的距离
    ax.set_title(classes[labels8[idx].item()], fontsize=10, pad=10)
    # 关闭坐标轴显示
    ax.axis('off')

# 调整子图间距，避免子图之间重叠
plt.tight_layout()
# 显示绘制好的图像
plt.show()
# 将图像保存为 "fashionmnist.png" 文件
plt.savefig("fashionmnist.png")
