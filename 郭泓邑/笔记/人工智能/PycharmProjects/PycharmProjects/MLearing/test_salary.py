import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# 补充知识点：
# 线性回归模型：因变量y是连续值预测的问题，结果是一个具体的 数值
# 线性回顾模型场景：预测薪资，预测评分，预测房价等具体数值问题

# 梯度下降法补充知识点：
# SGDRegressor: 使用随机梯度下降的线性回归模型
# 优点：适合大数据集，支持在线学习，内存效率高
# 缺点：需要调参，对特征缩放敏感

# 读取数据文件
df = pd.read_csv("salary_data.csv")

# 删除目标变量 预测就是薪资（目标变量）
data = df.drop("月均薪资", axis=1)
target = df["月均薪资"]  # 是一个连续的值

# ============= 特征工程 =============
# 定义特征类型
数值类型特征列 = ["工作年限", "绩效评分"]
分类类型特征列 = ["职位等级", "学历水平"]

# 构建预处理管道 列转换器处理数据的特征，等数据来时自动处理
# 对数值特征标准化：工作年限、绩效评分等数值特征,使用StandardScaler()将其转换为均值为0，方差为1的标准分 # 布。梯度下降对特征尺度敏感，标准化能加速收敛
# 对分类特征独热编码：职位等级、学历水平等分类特征使用OneHotEncoder()转换为二进制向量，机器学习模型不能直接处理文本类别
prePip = ColumnTransformer(
    transformers=[
        # 几类特征，组装几个管道
        # 处理数值类型特征的管道
        ("num", StandardScaler(), 数值类型特征列),  # 三元组
        # 处理类别类型特征的管道
        ("cat", OneHotEncoder(handle_unknown="ignore"), 分类类型特征列)
    ]
)

# 构建梯度下降模型 - 使用SGDRegressor替代LinearRegression
model = Pipeline(
    steps=[
        # 特征处理的管道
        ("prePip", prePip),
        # 梯度下降回归模型 - 替代线性回归
        ("regressor", SGDRegressor(
            loss='squared_error',  # 使用平方损失，等同于普通线性回归
            penalty='l2',  # L2正则化，防止过拟合
            alpha=0.0001,  # 正则化强度
            learning_rate='invscaling',  # 学习率调度策略
            eta0=0.01,  # 初始学习率
            max_iter=1000,  # 最大迭代次数
            tol=1e-3,  # 收敛容忍度
            random_state=42,  # 随机种子
            early_stopping=False,  # 不使用早停
            validation_fraction=0.1,  # 验证集比例（如果使用早停）
            n_iter_no_change=5  # 无改进迭代次数（如果使用早停）
        ))
    ]
)

# 划分数据集
(X_train,  # 80%训练集
 X_test,  # 20%测试集
 y_train,  # 80%训练集对应的目标变量
 y_test  # 20%测试集对应的目标变量
 ) = train_test_split(
    data, target, train_size=0.8,
    random_state=42
)

print("=" * 60)
print("🎯 梯度下降回归模型训练")
print("=" * 60)
print(f"训练集大小: {X_train.shape[0]}")
print(f"测试集大小: {X_test.shape[0]}")
print(f"特征数量: {X_train.shape[1]}")

# 训练模型
print("\n开始训练梯度下降模型...")
model.fit(X_train, y_train)

# 获取训练过程中的信息（如果可用）
if hasattr(model.named_steps['regressor'], 'n_iter_'):
    print(f"实际迭代次数: {model.named_steps['regressor'].n_iter_}")

# 预测
y_pred = model.predict(X_test)

# 模型评估
print("\n📊 模型评估结果:")
print("-" * 40)

# 计算各种评估指标
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"均方误差 (MSE): {mse:.2f}")
print(f"均方根误差 (RMSE): {rmse:.2f}")
print(f"平均绝对误差 (MAE): {mae:.2f}")
print(f"决定系数 (R²): {r2:.4f}")

# 计算平均误差百分比
mean_salary = np.mean(y_test)
error_percentage = (mae / mean_salary) * 100
print(f"平均绝对误差占平均薪资的: {error_percentage:.2f}%")

# 获取模型系数信息
regressor = model.named_steps['regressor']
print(f"\n🔍 模型参数信息:")
print(f"最终学习率: {regressor.eta0}")  # 注意：对于invscaling，这是初始学习率
print(f"使用的损失函数: {regressor.loss}")
print(f"正则化类型: {regressor.penalty}")
print(f"正则化强度: {regressor.alpha}")

# 保存模型
joblib.dump(model, "sgd_model.pkl")
print(f"\n💾 模型已保存为: sgd_model.pkl")

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决负号显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False


# 绘制预测结果
def plot_sgd_regression(y_test, y_pred, model_name="梯度下降回归"):
    """绘制梯度下降回归的预测结果"""

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

    # 1. 预测 vs 实际值散点图
    ax1.scatter(y_test, y_pred, alpha=0.6, color='blue')
    # 完美预测线
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    ax1.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='完美预测')
    ax1.set_xlabel('实际薪资')
    ax1.set_ylabel('预测薪资')
    ax1.set_title(f'{model_name} - 预测效果对比\nR² = {r2:.4f}')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 残差图
    residuals = y_test - y_pred
    ax2.scatter(y_pred, residuals, alpha=0.6, color='green')
    ax2.axhline(y=0, color='red', linestyle='--', linewidth=2)
    ax2.set_xlabel('预测薪资')
    ax2.set_ylabel('残差 (实际-预测)')
    ax2.set_title('残差分析图')
    ax2.grid(True, alpha=0.3)

    # 3. 误差分布直方图
    ax3.hist(residuals, bins=30, alpha=0.7, color='orange', edgecolor='black')
    ax3.axvline(x=0, color='red', linestyle='--', linewidth=2, label='零误差线')
    ax3.set_xlabel('预测误差')
    ax3.set_ylabel('频数')
    ax3.set_title('预测误差分布')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 实际值 vs 预测值折线图（按排序后的索引）
    sorted_indices = np.argsort(y_test)
    y_test_sorted = y_test.iloc[sorted_indices].values
    y_pred_sorted = y_pred[sorted_indices]

    ax4.plot(range(len(y_test_sorted)), y_test_sorted, 'b-', label='实际薪资', alpha=0.7)
    ax4.plot(range(len(y_pred_sorted)), y_pred_sorted, 'r--', label='预测薪资', alpha=0.7)
    ax4.set_xlabel('样本序号 (按实际薪资排序)')
    ax4.set_ylabel('薪资')
    ax4.set_title('实际薪资 vs 预测薪资趋势')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("梯度下降_薪资预测效果分析.png", dpi=300, bbox_inches='tight')
    plt.show()


# 调用函数绘制梯度下降回归的结果
plot_sgd_regression(y_test, y_pred)


# 模型调优建议函数
def 模型调优建议(当前r2, y_test, y_pred):
    """提供模型调优建议"""

    print("\n" + "=" * 60)
    print("🔧 模型调优建议")
    print("=" * 60)

    # 分析当前性能
    if r2 > 0.8:
        print("✅ 当前模型性能优秀 (R² > 0.8)")
    elif r2 > 0.6:
        print("📈 当前模型性能良好 (R² > 0.6)")
    elif r2 > 0.4:
        print("⚠️  当前模型性能一般 (R² > 0.4)，建议调优")
    else:
        print("❌ 当前模型性能较差 (R² ≤ 0.4)，需要调优")

    # 计算误差统计
    residuals = y_test - y_pred
    residual_std = np.std(residuals)

    print(f"\n📊 误差分析:")
    print(f"残差标准差: {residual_std:.2f}")
    print(f"最大正误差: {residuals.max():.2f}")
    print(f"最大负误差: {residuals.min():.2f}")

    # 调优建议
    print(f"\n💡 梯度下降调优建议:")

    if residual_std > np.std(y_test) * 0.5:
        print("1. 尝试减小学习率 (eta0=0.001) 以获得更稳定的收敛")
    else:
        print("1. 当前学习率设置合理")

    if r2 < 0.6:
        print("2. 增加最大迭代次数 (max_iter=2000)")
        print("3. 尝试不同的学习率调度策略: 'constant' 或 'adaptive'")
        print("4. 调整正则化强度 alpha (尝试 0.001 或 0.00001)")

    print("5. 考虑添加多项式特征或交互项")
    print("6. 检查特征工程，可能需要更多相关特征")


# 调用调优建议函数
模型调优建议(r2, y_test, y_pred)

print("\n" + "=" * 60)
print("🎉 梯度下降回归分析完成!")
print("=" * 60)
print("总结:")
print(f"- 使用SGDRegressor替代LinearRegression")
print(f"- 模型R²得分: {r2:.4f}")
print(f"- 模型已保存: sgd_model.pkl")
print(f"- 可视化结果已保存: 梯度下降_薪资预测效果分析.png")
print("\n下一步建议:")
print("1. 根据调优建议调整超参数")
print("2. 尝试不同的特征工程方法")
print("3. 考虑使用交叉验证选择最佳参数")