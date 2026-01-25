from sklearn.cluster import DBSCAN
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Simhei']
# 解决负号显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False
# 示例：使用共享单车数据


def my_dbscan(data, eps_value, k):
    # 使用k-距离图确定的参数
    optimal_eps = eps_value  # 从前面计算得到
    min_samples = k + 1  # k是最近邻数量
    # 应用DBSCAN
    db = DBSCAN(eps=optimal_eps, min_samples=min_samples )
    db.fit(data)
    # 获取聚类结果
    labels = db.labels_
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    print(f"发现聚类数: {n_clusters}")
    print(f"噪声点数: {n_noise}")
    # 可视化结果
    plt.figure(figsize=(12, 8))
    plt.scatter(data[:, 1],
                data[:, 0],
                c=labels,
                cmap='viridis',
                edgecolor='k',
                alpha=0.5)
    plt.title(f'DBSCAN聚类结果 (eps={optimal_eps:.3f}km, min_samples={min_samples})')
    plt.xlabel('经度')
    plt.ylabel('纬度')
    plt.colorbar(label='聚类标签')
    plt.savefig("密度聚类分析的共享单车数据.png")
    plt.show()

if __name__ == '__main__':
    bike_df = pd.read_csv('../shared_bike_data.csv')
    data = bike_df[["纬度", "经度"]].values
    # 进行数据的标准化处理
    data = StandardScaler().fit_transform(data)
    my_dbscan(data,eps_value=0.21568,k=5)
