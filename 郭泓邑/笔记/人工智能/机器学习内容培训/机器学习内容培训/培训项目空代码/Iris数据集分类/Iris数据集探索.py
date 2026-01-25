# 导入必要的库
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')

# 设置中文字体和图形样式
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 1. 加载数据
print("\n1. 加载数据...")
iris = load_iris()
X = iris.data  # 获取数据
y = iris.target # 获取数据的标签
feature_names = iris.feature_names # 获取数据特征的名称
target_names = iris.target_names #获取数据特征的名称

# 创建DataFrame以便更好地查看数据
df = pd.DataFrame(X, columns=feature_names)
df['species'] = y
df['species_name'] = [target_names[i] for i in y]

print(f"数据集形状: {X.shape}")
print(f"特征名称: {feature_names}")
print(f"目标类别: {target_names}")
print("\n前5行数据:")
print(df.head())

# 2. 数据探索
print("\n2. 数据探索...")
print("\n数据集基本信息:")
print(df.describe())

print("\n各类别样本数量:")
print(df['species_name'].value_counts())

# 可视化数据分布
fig, axes = plt.subplots(2, 2, figsize=(8, 5))
fig.suptitle('Iris数据集特征分布', fontsize=16)
# 特征定义 花萼长度 花萼宽度  花瓣长度  花瓣宽度
features = ['sepal length (cm)', 'sepal width (cm)',
            'petal length (cm)', 'petal width (cm)']
colors = ['red', 'blue', 'green']

for i, feature in enumerate(features):
    row, col = i // 2, i % 2
    for species in range(3):
        species_data = df[df['species'] == species][feature]
        axes[row, col].hist(species_data, alpha=0.7,
                            label=target_names[species],
                            color=colors[species])
    axes[row, col].set_title(f'{feature}分布')
    axes[row, col].set_xlabel(feature)
    axes[row, col].set_ylabel('频数')
    axes[row, col].legend()

plt.tight_layout()
plt.show()

# 特征关系散点图
plt.figure(figsize=(8, 5))
for i, species in enumerate(target_names):
    plt.scatter(df[df['species_name'] == species]['petal length (cm)'],
                df[df['species_name'] == species]['petal width (cm)'],
                label=species, alpha=0.7)
plt.xlabel('花瓣长度 (cm)')
plt.ylabel('花瓣宽度 (cm)')
plt.title('花瓣长度与宽度的关系')
plt.legend()
plt.show()