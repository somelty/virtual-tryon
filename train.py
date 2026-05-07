'''
虚拟试衣系统的基于PyTorch深度学习框架的服装分类神经网络模型训练程序
2025.03: Created by Xu Xiaoyang, Zhang Hua
2025.05: Modified by Zhang Hua
  - 把模型类 FashionCNN 的定义提取出来，放到 model.py 中
  - 语法适配 PyTorch 2.x
  - 在 Windows 11 的 Python 3.12.x 和 PyTorch 2.7 中测试通过
  - 新增 GPU 加速支持
'''
# -------------------------------
# 导入必要的库
# -------------------------------
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

# 导入自定义的神经网络模型类
from model import FashionCNN

# ===================== 【修改1】定义训练设备：优先使用GPU，无GPU则用CPU =====================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"训练设备: {device}")  # 打印确认是否使用GPU
print("Starting...")

# -------------------------------
# 数据转换及加载数据集
# -------------------------------
transform_train = transforms.Compose([
    transforms.RandomAffine(
        degrees=15, translate=(0.1, 0.1), scale=(0.8, 1.2)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

transform_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# 加载训练集（添加GPU优化参数）
trainset = torchvision.datasets.FashionMNIST(
    root='./data',
    train=True,
    download=True,
    transform=transform_train
)

# ===================== 【修改2】优化DataLoader，加速GPU数据加载 =====================
trainloader = torch.utils.data.DataLoader(
    trainset,
    batch_size=64,
    shuffle=True,
    num_workers=0,        # Windows系统必须设0，避免报错
    pin_memory=True       # GPU训练专用优化
)

# 加载测试集
testset = torchvision.datasets.FashionMNIST(
    root='./data',
    train=False,
    download=True,
    transform=transform_test
)

testloader = torch.utils.data.DataLoader(
    testset,
    batch_size=1000,
    shuffle=False,
    num_workers=0,
    pin_memory=True
)

# ===================== 【修改3】模型迁移到GPU =====================
net = FashionCNN().to(device)

# -------------------------------
# 损失函数和优化器（支持混合精度）
# -------------------------------
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=0.001)

# -------------------------------
# 训练模型并记录损失与准确率
# -------------------------------
num_epochs = 10          # 训练轮次
train_loss_history = []  # 用于保存每个epoch的平均训练损失
test_acc_history = []    # 用于保存每个epoch在测试集上的准确率

print(net)
print(f"Training on {num_epochs} epochs")

for epoch in range(num_epochs):
    net.train()  # 设置为训练模式
    epoch_loss = 0.0   # 当前epoch累计的损失
    print_loss = 0.0   # 用于每100个batch打印平均损失
    batch_count = 0    # 记录batch数量

    for i, (inputs, labels) in enumerate(trainloader):
        # ===================== 【修改4】数据迁移到GPU =====================
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()       # 清零梯度
        outputs = net(inputs)       # 前向传播
        loss = criterion(outputs, labels)
        loss.backward()             # 反向传播
        optimizer.step()            # 参数更新

        loss_val = loss.item()
        epoch_loss += loss_val     # 累计损失
        print_loss += loss_val
        batch_count += 1

        if i % 100 == 99:
            print(f'[Epoch {epoch+1}, Batch {i+1}] loss: {print_loss/100:.3f}')
            print_loss = 0.0

    # 计算本epoch的平均训练损失
    avg_loss = epoch_loss / batch_count
    train_loss_history.append(avg_loss)

    # 在测试集上评估模型
    net.eval()  # 设置为评估模式
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in testloader:
            # ===================== 【修改5】测试数据迁移到GPU =====================
            images, labels = images.to(device), labels.to(device)

            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    acc = 100 * correct / total
    test_acc_history.append(acc)
    print(f'Epoch {epoch+1}: Test Accuracy: {acc:.2f}%')

# 保存模型状态字典（推荐方式）
torch.save(net.state_dict(), './cnn_model.pth')

print('Finished Training')

# -------------------------------
# 可视化结果：绘制训练损失和测试准确率曲线
# -------------------------------
epochs = range(1, num_epochs + 1)

plt.figure()
plt.plot(epochs, train_loss_history, 'r-', label='Training Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss over Epochs')
plt.xticks(epochs)
plt.legend()
plt.savefig('cnn_loss.png')

plt.figure()
plt.plot(epochs, test_acc_history, 'b-', label='Test Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy (%)')
plt.title('Test Accuracy over Epochs')
plt.xticks(epochs)
plt.legend()
plt.savefig('cnn_acc.png')
