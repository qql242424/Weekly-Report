# 1. 导入必要的库
import tensorflow as tf
from tensorflow import keras
from keras import layers, models
import matplotlib.pyplot as plt
import numpy as np

# 2. 加载并预处理数据集 (MNIST)
# MNIST 是一个经典的手写数字数据集，包含 60,000 张训练图片和 10,000 张测试图片
# Keras 内置了加载 MNIST 的函数，非常方便
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# 数据预处理
# 2.1 将像素值归一化到 0 和 1 之间。原始像素值是 0-255 的整数。
# 归一化可以帮助模型更快、更稳定地收敛。
x_train = x_train / 255.0
x_test = x_test / 255.0

# 2.2 打印数据集的形状，了解数据结构
print(f"训练集图片形状: {x_train.shape}")  # 输出 (60000, 28, 28)，即 60000 张 28x28 的灰度图
print(f"训练集标签形状: {y_train.shape}")  # 输出 (60000,)，即 60000 个标签
print(f"测试集图片形状: {x_test.shape}")  # 输出 (10000, 28, 28)
print(f"测试集标签形状: {y_test.shape}")  # 输出 (10000,)

# 2.3 (可选) 可视化一张图片，看看数据长什么样
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows
plt.figure(figsize=(10, 1))
plt.imshow(x_train[0], cmap='gray')
plt.title(f"Label: {y_train[0]}")
plt.axis('off')
plt.show()

# 3. 构建深层神经网络模型
# 我们使用 Sequential 模型，它是一个线性的层堆叠
model = models.Sequential()

# 3.1 输入层：Flatten 层
# 我们的输入是 28x28 的二维数组，但全连接层需要一维的向量作为输入。
# Flatten 层的作用就是将 28x28 的矩阵“展平”成一个 784 个元素的一维向量 (28*28=784)。
model.add(layers.Flatten(input_shape=(28, 28)))

# 3.2 隐藏层：Dense 层
# Dense 层是全连接层，每个神经元都与上一层的所有神经元相连。
# 第一个隐藏层有 128 个神经元，激活函数使用 ReLU (Rectified Linear Unit)。
# ReLU 是目前最常用的激活函数之一，它能有效解决梯度消失问题。
model.add(layers.Dense(128, activation='relu'))

# 3.3 第二个隐藏层 (可选)
# 增加更多的层和神经元可以让模型学习更复杂的模式，但也会增加计算量和过拟合的风险。
# 这里我们再增加一个有 64 个神经元的隐藏层。
model.add(layers.Dense(64, activation='relu'))

# 3.4 输出层：Dense 层
# 输出层需要 10 个神经元，对应 0-9 这 10 个数字。
# 激活函数使用 softmax，它可以将输出值转换为一个概率分布，所有输出值的和为 1。
# 这样，模型会输出它认为输入图片属于每个数字的概率。
model.add(layers.Dense(10, activation='softmax'))

# 3.5 查看模型结构
model.summary()

# 4. 编译模型
# 在训练模型之前，我们需要配置它的学习过程。
model.compile(
    optimizer='adam',  # 优化器，adam 是一种常用的、自适应学习率的优化器
    loss='sparse_categorical_crossentropy',  # 损失函数
    # 因为我们的标签是整数 (如 5, 3)，而不是 one-hot 编码 (如 [0,0,0,0,0,1,0,0,0,0])，
    # 所以使用 sparse_categorical_crossentropy 更方便。
    metrics=['accuracy']  # 评估指标，我们关注准确率
)

# 5. 训练模型
# fit() 函数开始训练过程
# x_train 和 y_train 是训练数据和标签
# epochs: 训练的轮数，即整个训练数据集将被模型“学习”多少次
# batch_size: 每次训练时，模型会从数据集中取 batch_size 个样本进行梯度下降更新
# validation_split: 从训练集中划分出 20% 的数据作为验证集，用于在训练过程中评估模型性能，防止过拟合
history = model.fit(x_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# 6. 评估模型
# 使用测试集来评估模型在新数据上的泛化能力
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"\n模型在测试集上的准确率: {test_acc:.4f}")

# 6.1 (可选) 绘制训练过程中的准确率和损失变化曲线
plt.figure(figsize=(12, 4))

# 绘制准确率曲线
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='训练准确率')
plt.plot(history.history['val_accuracy'], label='验证准确率')
plt.title('准确率变化')
plt.xlabel('Epoch')
plt.ylabel('准确率')
plt.legend()

# 绘制损失曲线
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='训练损失')
plt.plot(history.history['val_loss'], label='验证损失')
plt.title('损失变化')
plt.xlabel('Epoch')
plt.ylabel('损失')
plt.legend()

plt.show()

# 7. 使用模型进行预测
# 从测试集中随机挑选几张图片，用我们训练好的模型进行预测，看看效果如何
predictions = model.predict(x_test)

# 随机选择 5 张图片
num_predictions = 5
random_indices = np.random.choice(len(x_test), num_predictions)

plt.figure(figsize=(15, 3))
for i, idx in enumerate(random_indices):
    plt.subplot(1, num_predictions, i + 1)
    plt.imshow(x_test[idx], cmap='gray')
    plt.axis('off')

    # 模型预测的结果是一个包含 10 个概率值的数组，argmax 可以找出概率最大的那个索引，即预测的数字
    predicted_label = np.argmax(predictions[idx])
    true_label = y_test[idx]

    # 如果预测正确，标题为绿色，否则为红色
    color = 'green' if predicted_label == true_label else 'red'
    plt.title(f"预测: {predicted_label}\n真实: {true_label}", color=color)

plt.show()