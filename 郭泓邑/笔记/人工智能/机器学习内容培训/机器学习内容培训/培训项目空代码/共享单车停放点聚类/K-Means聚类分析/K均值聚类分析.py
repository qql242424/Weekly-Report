import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Simhei']
# 解决负号显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

def get_k_value(data):
    # 使用肘部法则确定最佳K值
    # 创建一个字典，用于存储每个k值对应的轮廓系数得分
    k_sl_score = {}
    # 遍历每个k值
    for k in range(2, 10):
        # 创建KMeans模型
        kmeans = KMeans(n_clusters=k, random_state=42)
        # 训练模型
        kmeans.fit(data)
        # 计算轮廓系数
        sl_score = silhouette_score(data, kmeans.labels_)
        # 将轮廓系数和惯性值添加到列表中
        k_sl_score[k] = sl_score
    # end for
    # 找到字典k_sl_score中值最大对应的key值
    best_k = max(k_sl_score, key=k_sl_score.get)
    print('最佳K值:', best_k)
    return best_k,k_sl_score


def my_KMeans(k, data):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data)
    return kmeans.labels_, kmeans.cluster_centers_

def plot_cluster_result(data,centers,pred_target,best_k,k_sl_score):
    ''' 可视化聚类结果'''
    plt.figure(figsize=(12, 5))
    # 绘制1行3列中的第1个子图
    # ======== 绘制原始数据分布 ========
    plt.subplot(1, 3, 1)
    plt.scatter(data[:, 0],data[:, 1],
                edgecolor='k',s=30)
    plt.xlabel('经度(标准化)')
    plt.ylabel('经度(标准化)')
    plt.title('原始数据分布图')
    plt.subplot(1, 3, 2)
    # ======== 绘制最佳K值的确定 ========
    plt.plot(  # 绘制轮廓系数得分曲线
        k_sl_score.keys(),
        k_sl_score.values(),
        'bx-')
    plt.scatter(best_k,
                k_sl_score[best_k],
                color='red', s=40,
                )
    plt.xlabel('聚类促中心点个数')
    plt.ylabel('轮廓系数得分')
    plt.title('使用肘部法则确定最佳K值')
    plt.grid(True)
    # ======== 绘制最终的聚类结果 ========
    plt.subplot(1, 3, 3)
    for i in range(best_k):
        plt.scatter(data[pred_target == i, 0],
                    data[pred_target == i, 1],
                    edgecolor='k',
                    label=f'中心点 {i}')
    # 绘制中心点
    plt.scatter(centers[:, 0],centers[:, 1],
                s=300,c='red',
                marker='*',label='聚类中心点')
    plt.title(f'K-means 聚类 (K={best_k})')
    plt.xlabel('经度(标准化)')
    plt.ylabel('维度(标准化)')
    plt.legend( )
    plt.tight_layout()
    plt.savefig('K-means聚类分析共享单车数据.png')
    plt.show()

if __name__ == '__main__':
    bike_df = pd.read_csv('../shared_bike_data.csv')
    data = bike_df[["纬度", "经度"]]

    # 进行数据的标准化处理
    data = StandardScaler().fit_transform(data)
    best_k, k_sl_score = get_k_value(data)
    # 使用KMeans模型对数据进行聚类
    pred_target,centers= my_KMeans(best_k, data)
    plot_cluster_result(data, centers, pred_target, best_k, k_sl_score)

