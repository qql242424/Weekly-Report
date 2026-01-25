# 构造符合格式的测试数据（确保与训练数据格式完全一致）
import joblib
import pandas as pd
# 构造的测试数据
test_data = {
    '职位等级': ['高级工程师'],
    '工作年限': [6.5],        # 保留1位小数
    '学历水平': ['硕士'],
    '绩效评分': [4.75]        # 保留2位小数
}
# 转换为DataFrame
input_df = pd.DataFrame(test_data)
# 加载模型
model = joblib.load("sgd_model.pkl")
# 进行预测
predicted_salary = model.predict(input_df)
print("\n预测月薪：￥{:.2f}".format(predicted_salary[0]))