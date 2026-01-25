import pandas as pd
import numpy as np

# Series创建
s1 = pd.Series([1, 3, 5, np.nan, 6, 8])
s2 = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
s3 = pd.Series({'北京': 2154, '上海': 2428, '深圳': 1756})

print("Series基本操作:")
print(s2.values)    # 值数组
print(s2.index)     # 索引
print(s2['b'])      # 索引访问

# DataFrame创建
data = {
    '城市': ['北京', '上海', '广州', '深圳', '杭州'],
    '人口_万': [2189, 2428, 1868, 1756, 1194],
    'GDP_亿元': [36103, 38701, 25019, 27670, 16106],
    '增长率': [0.065, 0.068, 0.072, 0.069, 0.081]
}

df = pd.DataFrame(data)
print("DataFrame基本信息:")
print(df.shape)           # 形状
print(df.columns)         # 列名
print(df.dtypes)          # 数据类型
print(df.head(3))         # 前3行

# 创建示例数据集
df = pd.DataFrame({
    '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
    '年龄': [25, 32, 28, 45, 36],
    '城市': ['北京', '上海', '广州', '北京', '深圳'],
    '薪资': [15000, 22000, 18000, 35000, 28000],
    '部门': ['技术', '销售', '技术', '管理', '销售']
})

print("数据探索:")
print(df.info())          # 数据信息
print(df.describe())      # 统计描述