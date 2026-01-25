import pandas as pd
from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
import joblib
from sklearn.model_selection import GridSearchCV
import warnings

# ================= 模型参数优化 =================
def model_optimization(X_train, y_train, model):
    param_grid = {
        'classifier__C': [0.001, 0.01, 0.1, 1, 10],
        'classifier__penalty': ['l1', 'l2'],
        'classifier__solver': ['liblinear', 'saga','lbfgs'],
        'classifier__max_iter': [100,  1000]
    }
    # 忽略收敛警告
    with warnings.catch_warnings():
        print("正在参数寻优中......")
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        grid_search = GridSearchCV(model, param_grid, cv=5)
        grid_search.fit(X_train, y_train)
        print("最优参数:", grid_search.best_params_)
    return grid_search


def feature_engineering():
    # ================= 特征工程 =================
    # 定义特征类型
    numeric_features = ["年龄", "收入", "负债比率"]
    categorical_features = ["工作类型", "信用历史"]

    # 构建预处理管道
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
        ])
    return preprocessor

# ================= 逻辑回归模型训练 =================
def train_logistic_regression(X, y):
    # ================= 训练数据划分 =================
    X_train, X_test, y_train, y_test = (
        train_test_split(X, y,
                         test_size=0.2,
                         stratify=y,
                         random_state=42))
    preprocessor = feature_engineering()
    pipline = Pipeline(
        steps=[("preprocessor", preprocessor),
               ("classifier", LogisticRegression())]
    )
    # ================= 进行模型的参数寻优 根据寻优结果重新定义 =================
    grid_search = model_optimization(X_train, y_train, pipline)
    # 训练模型
    best_model = grid_search.best_estimator_

    best_model.fit(X_train, y_train)
    # ================= 模型训练模型 =================
    y_pred = best_model.predict(X_test)
    y_proba = best_model.predict_proba(X_test)[:, 1]

    # ================ 训练模型的评估  =================
    print("测试集准确率:",
          round(accuracy_score(y_test, y_pred),3)
          )

    print("\n分类报告:")
    print(classification_report(y_test, y_pred,target_names=['优','差']))
    print("\nAUC-ROC:", round(roc_auc_score(y_test, y_proba),3))

    # 保存训练好的模型
    joblib.dump(best_model, 'credit_prediction_model.joblib')

if __name__ == '__main__':
    # 读取训练数据
    train_data = pd.read_csv('train_data_set/customer_credit_data_train.csv')
    # 定义特征和目标变量
    X = train_data.drop('信用标签', axis=1)
    y = train_data['信用标签']
    # 进行逻辑回归模型训练
    train_logistic_regression(X, y)
    print("模型训练完成！")
