import joblib
import pandas as pd
def predict_credit(test_data):
    # 加载模型
    model = joblib.load("credit_prediction_model.joblib")
    # 使用模型进行预测
    prediction = model.predict(test_data)
    return prediction

if __name__ == '__main__':
    # 读取测试数据
    test_data = pd.read_csv('train_data_set/customer_credit_data_test.csv')
    prediction = predict_credit(test_data)
    test_data["预测结果"] = prediction
    print("测试数据：", prediction)
    test_data.to_csv("pred_data_set/customer_credit_data_test_result.csv",
                     index=False)