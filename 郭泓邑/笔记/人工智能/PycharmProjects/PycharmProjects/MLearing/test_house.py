import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 读取数据
house_data = pd.read_csv("house.csv")


# 数据探索分析
def 数据探索分析(数据):
    """全面分析数据集"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))

    # 1. 房价分布
    axes[0, 0].hist(数据['房价'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].set_xlabel('房价 (万元)')
    axes[0, 0].set_ylabel('频数')
    axes[0, 0].set_title('房价分布')
    axes[0, 0].grid(True, alpha=0.3)

    # 2. 面积 vs 房价
    axes[0, 1].scatter(数据['面积'], 数据['房价'], alpha=0.6)
    axes[0, 1].set_xlabel('面积 (㎡)')
    axes[0, 1].set_ylabel('房价 (万元)')
    axes[0, 1].set_title('面积 vs 房价')
    axes[0, 1].grid(True, alpha=0.3)

    # 3. 卧室数量 vs 平均房价
    卧室均价 = 数据.groupby('卧室数量')['房价'].mean()
    axes[0, 2].bar(卧室均价.index, 卧室均价.values, color='lightgreen', alpha=0.7)
    axes[0, 2].set_xlabel('卧室数量')
    axes[0, 2].set_ylabel('平均房价 (万元)')
    axes[0, 2].set_title('卧室数量 vs 平均房价')
    axes[0, 2].grid(True, alpha=0.3)

    # 4. 建造年份 vs 房价
    axes[1, 0].scatter(数据['建造年份'], 数据['房价'], alpha=0.6, color='orange')
    axes[1, 0].set_xlabel('建造年份')
    axes[1, 0].set_ylabel('房价 (万元)')
    axes[1, 0].set_title('建造年份 vs 房价')
    axes[1, 0].grid(True, alpha=0.3)

    # 5. 距离市中心 vs 房价
    axes[1, 1].scatter(数据['距离市中心'], 数据['房价'], alpha=0.6, color='red')
    axes[1, 1].set_xlabel('距离市中心 (km)')
    axes[1, 1].set_ylabel('房价 (万元)')
    axes[1, 1].set_title('距离市中心 vs 房价')
    axes[1, 1].grid(True, alpha=0.3)

    # 6. 相关性热力图
    correlation = 数据.corr()
    sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, ax=axes[1, 2])
    axes[1, 2].set_title('特征相关性热力图')

    plt.tight_layout()
    plt.show()

    # 打印相关性分析
    print("\n🔍 特征与房价的相关性:")
    correlations = 数据.corr()['房价'].sort_values(ascending=False)
    for feature, corr in correlations.items():
        if feature != '房价':
            direction = "正相关" if corr > 0 else "负相关"
            print(f"  {feature}: {corr:.3f} ({direction})")
数据探索分析(house_data)

# 准备特征和目标变量
X = house_data[['面积', '卧室数量', '楼层', '建造年份', '距离市中心']]
y = house_data['房价']

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 创建并训练线性回归模型
model = LinearRegression()
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 模型评估
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("=== 线性回归模型评估 ===")
print(f"均方误差(MSE): {mse:.2f}")
print(f"均方根误差(RMSE): {rmse:.2f}")
print(f"决定系数(R²): {r2:.4f}")

# 显示模型系数
feature_names = ['面积', '卧室数量', '楼层', '建造年份', '距离市中心']
coefficients = pd.DataFrame({
    '特征': feature_names,
    '系数': model.coef_
}).sort_values('系数', ascending=False)

print("\n=== 特征重要性 ===")
print(coefficients)

# 预测结果可视化
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# 1. 实际值 vs 预测值
ax1.scatter(y_test, y_pred, alpha=0.7)
ax1.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
ax1.set_xlabel('实际房价(万)')
ax1.set_ylabel('预测房价(万)')
ax1.set_title(f'实际值 vs 预测值 (R² = {r2:.4f})')

# 2. 残差图
residuals = y_test - y_pred
ax2.scatter(y_pred, residuals, alpha=0.7)
ax2.axhline(y=0, color='r', linestyle='--')
ax2.set_xlabel('预测房价(万)')
ax2.set_ylabel('残差')
ax2.set_title('残差图')

plt.tight_layout()
plt.show()

# 模型诊断
print("\n=== 模型诊断 ===")
print(f"平均绝对误差: {np.mean(np.abs(residuals)):.2f}")
print(f"残差标准差: {np.std(residuals):.2f}")