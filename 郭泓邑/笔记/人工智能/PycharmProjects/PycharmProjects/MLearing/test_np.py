# Python列表 vs NumPy数组
import time

# Python列表操作
python_list = list(range(1000000))
start = time.time()
result = [x * 2 for x in python_list]
end = time.time()
print(f"Python列表耗时: {end - start:.4f}秒")

# NumPy数组操作
import numpy as np
numpy_array = np.arange(1000000)
start = time.time()
result = numpy_array * 2
end = time.time()
print(f"NumPy数组耗时: {end - start:.4f}秒")

import numpy as np
# 基本数学运算
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print("加法:", a + b)
print("乘法:", a * b)
print("点积:", np.dot(a, b))
print("求和:", np.sum(a))
print("平均值:", np.mean(a))
print("标准差:", np.std(a))

matrix = np.array([[1, 2, 3], [4, 5, 6]])
print("形状:", matrix.shape)
print("重塑:", matrix.reshape(3, 2))
print("转置:", matrix.T)

# 广播示例
a = np.array([[1, 2, 3], [4, 5, 6]])
b = np.array([10, 20, 30])

# 小数组自动扩展匹配大数组形状
result = a + b
print("广播结果:")
print(result)