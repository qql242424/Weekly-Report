import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
# 创建数据网格
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)

# 定义多元函数
Z1 = np.exp(-(X**2 + Y**2)) * np.sin(2*X) * np.cos(2*Y)
Z2 = np.sin(X**2 + Y**2) / (X**2 + Y**2 + 0.1)

# 创建图形
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('多维数据表面可视化', fontsize=16, fontweight='bold')

# 热力图
im1 = ax1.imshow(Z1, extent=[-3, 3, -3, 3], origin='lower', cmap='hot', aspect='auto')
ax1.set_title('热力图', fontsize=14)
ax1.set_xlabel('X轴')
ax1.set_ylabel('Y轴')
plt.colorbar(im1, ax=ax1, shrink=0.8)

# 等高线图
contour = ax2.contour(X, Y, Z2, levels=15, colors='black', alpha=0.6)
ax2.clabel(contour, inline=True, fontsize=8)
im2 = ax2.contourf(X, Y, Z2, levels=50, cmap='plasma', alpha=0.7)
ax2.set_title('等高线图', fontsize=14)
ax2.set_xlabel('X轴')
ax2.set_ylabel('Y轴')
plt.colorbar(im2, ax=ax2, shrink=0.8)

# 填充等高线图
im3 = ax3.contourf(X, Y, Z1, levels=50, cmap='viridis')
ax3.contour(X, Y, Z1, levels=10, colors='black', linewidths=0.5)
ax3.set_title('填充等高线图', fontsize=14)
ax3.set_xlabel('X轴')
ax3.set_ylabel('Y轴')
plt.colorbar(im3, ax=ax3, shrink=0.8)

plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.show()