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
# 2. 数据预处理
print("\n2. 数据集划分与标准化处理...")
# 分割数据集
(X_train, X_test,
 y_train, y_test) = train_test_split(X, y,
                                     test_size=0.2,
                                     random_state=42)
# 标准化特征（决策树通常不需要，但为了演示标准化过程）
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"训练集大小: {X_train.shape}")
print(f"测试集大小: {X_test.shape}")

# 3. 训练决策树模型
print("\n3. 训练决策树模型...")
# 创建决策树分类器
dt_classifier = DecisionTreeClassifier(random_state=42)

# 定义参数网格
param_grid = {
    'max_depth': [3, 5, 7, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'criterion': ['gini', 'entropy']
}

# 使用网格搜索寻找最佳参数
print("正在进行参数调优...")
grid_search = GridSearchCV(
    dt_classifier,
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1)
grid_search.fit(X_train, y_train)

# 获取最佳模型
best_dt = grid_search.best_estimator_

print(f"最佳参数: {grid_search.best_params_}")
print(f"最佳交叉验证分数: {grid_search.best_score_:.4f}")

# 4. 模型评估
print("\n4. 模型评估...")
# 在训练集和测试集上进行预测
y_train_pred = best_dt.predict(X_train)
y_test_pred = best_dt.predict(X_test)

# 计算准确率
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

print(f"训练集准确率: {train_accuracy:.4f}")
print(f"测试集准确率: {test_accuracy:.4f}")

# 分类报告
print("\n分类报告:")
print(classification_report(y_test, y_test_pred, target_names=target_names))


# 5. 可视化决策树
print("\n5. 可视化决策树...")
plt.figure(figsize=(10, 8))
plot_tree(best_dt,
          feature_names=feature_names,
          class_names=target_names,
          filled=True,
          rounded=True,
          fontsize=12)
plt.title('决策树结构')
plt.show()

# 打印文本形式的决策树规则
print("\n决策树规则:")
tree_rules = export_text(best_dt, feature_names=feature_names)
print(tree_rules)

# 6. 特征重要性分析
print("\n6. 特征重要性分析...")
feature_importance = best_dt.feature_importances_
feature_importance_df = pd.DataFrame({
    '特征': feature_names,
    '重要性': feature_importance
}).sort_values('重要性', ascending=False)

print("特征重要性排序:")
print(feature_importance_df)

# 7 使用模型进行预测
print("\n7. 使用模型进行预测...")
# 创建一些示例数据
# 特征定义 花萼长度sepal length 花萼宽度sepal width  花瓣长度petal length  花瓣宽度petal width
example_flowers = [
    [5.1, 3.5, 1.4, 0.2],  # 应该预测为setosa
    [6.0, 2.7, 5.1, 1.6],  # 应该预测为versicolor
    [7.2, 3.0, 5.8, 2.1]  # 应该预测为virginica
]

for i, flower in enumerate(example_flowers):
    prediction = best_dt.predict([flower])[0]
    probability = best_dt.predict_proba([flower])[0]

    print(f"\n示例花 {i + 1}: {flower}")
    print(f"预测类别: {target_names[prediction]}")
    print("类别概率:")
    for j, prob in enumerate(probability):
        print(f"  {target_names[j]}: {prob:.4f}")

# 8. 模型复杂度与性能关系
print("\n9. 分析不同树深度对性能的影响...")
max_depths = range(1, 11)
train_scores = []
test_scores = []

for depth in max_depths:
    dt_temp = DecisionTreeClassifier(max_depth=depth, random_state=42)
    dt_temp.fit(X_train, y_train)
    train_scores.append(accuracy_score(y_train, dt_temp.predict(X_train)))
    test_scores.append(accuracy_score(y_test, dt_temp.predict(X_test)))

plt.figure(figsize=(8, 6))
plt.plot(max_depths, train_scores, 'o-', label='训练集准确率')
plt.plot(max_depths, test_scores, 'o-', label='测试集准确率')
plt.xlabel('决策树深度')
plt.ylabel('准确率')
plt.title('决策树深度与性能关系')
plt.legend()
plt.grid(True)
plt.show()

print("\n" + "=" * 60)
print("模型训练和评估完成!")
print(f"最终测试集准确率: {test_accuracy:.4f}")
print("=" * 60)