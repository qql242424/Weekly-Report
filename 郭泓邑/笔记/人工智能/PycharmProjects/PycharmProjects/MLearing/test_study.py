import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建学习时间与成绩的模拟数据
np.random.seed(42)
学习时间 = np.linspace(1, 10, 100)  # 每天学习1-10小时
基础成绩 = 40
学习效果 = 6  # 每小时提升6分

真实成绩 = 基础成绩 + 学习效果 * 学习时间

# 添加现实中的随机因素（状态、题目难度等）
随机因素 = np.random.normal(0, 8, 100)
实际成绩 = 真实成绩 + 随机因素

print("=== 学习数据分析 ===")
print(f"数据量: {len(学习时间)} 名学生")
print(f"学习时间范围: {学习时间.min():.1f} - {学习时间.max():.1f} 小时")
print(f"成绩范围: {实际成绩.min():.1f} - {实际成绩.max():.1f} 分")


# 最小二乘法手动实现 - 直观版本
def 寻找最佳直线(x, y):
    """用最小二乘法找到最佳拟合直线"""
    # 计算平均值
    x平均 = np.mean(x)
    y平均 = np.mean(y)

    # 计算斜率（学习效率）
    分子 = np.sum((x - x平均) * (y - y平均))
    分母 = np.sum((x - x平均) ** 2)
    斜率 = 分子 / 分母

    # 计算截距（基础能力）
    截距 = y平均 - 斜率 * x平均

    return 截距, 斜率


# 应用最小二乘法
基础能力, 学习效率 = 寻找最佳直线(学习时间, 实际成绩)
预测成绩 = 基础能力 + 学习效率 * 学习时间
拟合优度 = r2_score(实际成绩, 预测成绩)

print("\n=== 最小二乘法分析结果 ===")
print(f"基础能力分数: {基础能力:.1f} 分")
print(f"学习效率: {学习效率:.1f} 分/小时")
print(f"模型解释度: {拟合优度:.1%}")
print("👉 解读: 每多学习1小时，成绩平均提高{:.1f}分".format(学习效率))


class 智能优化器:
    """梯度下降法的直观实现"""

    def __init__(self, 学习速度=0.01, 迭代次数=1000):
        self.学习速度 = 学习速度
        self.迭代次数 = 迭代次数
        self.当前基础能力 = 0
        self.当前学习效率 = 0
        self.损失记录 = []

    def 计算误差(self, x, y):
        """计算当前直线的预测误差"""
        预测值 = self.当前基础能力 + self.当前学习效率 * x
        误差 = (1 / (2 * len(x))) * np.sum((预测值 - y) ** 2)
        return 误差

    def 优化(self, x, y):
        """逐步优化参数"""
        数据量 = len(x)

        for 轮次 in range(self.迭代次数):
            # 当前预测
            预测成绩 = self.当前基础能力 + self.当前学习效率 * x

            # 计算调整方向
            调整基础能力 = (1 / 数据量) * np.sum(预测成绩 - y)
            调整学习效率 = (1 / 数据量) * np.sum((预测成绩 - y) * x)

            # 更新参数
            self.当前基础能力 -= self.学习速度 * 调整基础能力
            self.当前学习效率 -= self.学习速度 * 调整学习效率

            # 记录进展
            当前误差 = self.计算误差(x, y)
            self.损失记录.append(当前误差)

            if 轮次 % 200 == 0:
                print(f"第{轮次}轮: 误差 = {当前误差:.2f}")


# 使用梯度下降法优化
优化器 = 智能优化器(学习速度=0.01, 迭代次数=1000)
优化器.优化(学习时间, 实际成绩)

梯度下降预测 = 优化器.当前基础能力 + 优化器.当前学习效率 * 学习时间
梯度下降拟合优度 = r2_score(实际成绩, 梯度下降预测)

print("\n=== 梯度下降法分析结果 ===")
print(f"基础能力分数: {优化器.当前基础能力:.1f} 分")
print(f"学习效率: {优化器.当前学习效率:.1f} 分/小时")
print(f"模型解释度: {梯度下降拟合优度:.1%}")

# 创建对比可视化
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# 1. 数据与拟合线对比
ax1.scatter(学习时间, 实际成绩, alpha=0.6, label='学生实际数据', color='blue')
ax1.plot(学习时间, 真实成绩, 'g-', linewidth=3, label='真实规律', alpha=0.8)
ax1.plot(学习时间, 预测成绩, 'r-', linewidth=2,
         label=f'最小二乘法 (解释度:{拟合优度:.1%})')
ax1.plot(学习时间, 梯度下降预测, 'orange', linewidth=2,
         label=f'梯度下降法 (解释度:{梯度下降拟合优度:.1%})')
ax1.set_xlabel('学习时间 (小时/天)')
ax1.set_ylabel('考试成绩 (分)')
ax1.set_title('学习方法效果分析')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. 梯度下降优化过程
ax2.plot(优化器.损失记录)
ax2.set_xlabel('优化轮次')
ax2.set_ylabel('预测误差')
ax2.set_title('梯度下降优化过程')
ax2.text(0.6, 0.9, '误差逐渐减小\n找到最优解', transform=ax2.transAxes,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
ax2.grid(True, alpha=0.3)

# 3. 残差分析
最小二乘残差 = 实际成绩 - 预测成绩
梯度下降残差 = 实际成绩 - 梯度下降预测

ax3.scatter(预测成绩, 最小二乘残差, alpha=0.6, label='最小二乘法')
ax3.scatter(梯度下降预测, 梯度下降残差, alpha=0.6, label='梯度下降法')
ax3.axhline(y=0, color='black', linestyle='--', alpha=0.8)
ax3.set_xlabel('预测成绩')
ax3.set_ylabel('预测误差')
ax3.set_title('预测准确性分析')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 4. 方法对比总结
方法 = ['最小二乘法', '梯度下降法']
解释度 = [拟合优度, 梯度下降拟合优度]
颜色 = ['lightcoral', 'lightblue']

bars = ax4.bar(方法, 解释度, color=颜色, alpha=0.8)
ax4.set_ylabel('模型解释度 (R²)')
ax4.set_title('方法效果对比')
ax4.set_ylim(0, 1)
# 在柱子上添加数值
for bar, 值 in zip(bars, 解释度):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height + 0.02,
             f'{值:.1%}', ha='center', va='bottom')

plt.tight_layout()
plt.show()

# 实用建议
print("\n" + "="*50)
print("📊 学习建议分析")
print("="*50)
print(f"• 基础能力: {基础能力:.1f}分 (不学习也能得到的分数)")
print(f"• 学习效率: {学习效率:.1f}分/小时 (每小时的提升效果)")
print(f"• 建议学习时间: 6-8小时/天 (收益最佳的区间)")
print(f"• 模型可靠性: {拟合优度:.1%} (数据规律性的强度)")