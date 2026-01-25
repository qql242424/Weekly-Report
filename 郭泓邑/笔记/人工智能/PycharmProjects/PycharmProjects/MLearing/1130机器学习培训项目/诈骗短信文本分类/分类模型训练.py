import re
import jieba
import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

#加载停用词表
with open("data_set/stop_words.txt", "r", encoding="utf-8") as fr:
    stop_words = fr.read().split("\n")
    stop_words.append("\n")
# 用户词典
jieba.load_userdict("data_set/user_dict.txt")


def chinese_text_cut(text):
    text = re.sub("[^\u4e00-\u9fa5]", "", text)
    words = jieba.lcut(text)
    words = [wd for wd in words if wd not in stop_words and len(wd)>1]
    return words
# end chinese_text_cut(text)


def train_nb_model(data, tag):
    print("装载文本特征处理的函数...")
    # 进行向量化 文本的特征处理
    tfidf = TfidfVectorizer(
        tokenizer=chinese_text_cut,
        stop_words=stop_words,
        token_pattern=None
    )
    print("进行训练文本数据的划分...")
    # 划分训练集和测试集
    (X_train,
     X_test,
     y_train,
     y_test) = train_test_split(
        data, tag,
        test_size=0.2,
        random_state=1
    )
    print(f"训练集: {len(X_train)} 条")
    print(f"测试集: {len(X_test)} 条")
    # 构建Pipeline
    print("构建Pipeline流水线管道......")
    pipeline = Pipeline([
        ('tfidf', tfidf), # 先进行文本的处理
        ('nb', MultinomialNB(alpha=0.1)) # 之后调用模型进行分类处理
    ])

    # 训练模型
    print("开始训练模型...")
    pipeline.fit(X_train, y_train)

    # 评估模型
    print("评估训练的模型...")
    y_pred = pipeline.predict(X_test)
    train_accuracy = pipeline.score(X_train, y_train)
    test_accuracy = pipeline.score(X_test, y_test)

    print(f"训练集准确率: {train_accuracy:.4f}")
    print(f"测试集准确率: {test_accuracy:.4f}")
    print("分类报告\n",
          classification_report(y_test, y_pred)
    )
    # 保存模型和词袋
    print("保存模型......")
    joblib.dump(tfidf, "train_model/tfidf.pkl")
    print(f"TF-IDF向量化器已保存到: train_model目录下")
    joblib.dump(pipeline, 'train_model/sms_classifier.pkl')
    print("模型已保存在train_mode目录下")
# end train_nb_model




if __name__ == '__main__':
    df = pd.read_csv("data_set/Scam_text_message.csv")
    # ID,content,target
    tag = df["target"]
    data = df["content"]
    train_nb_model(data, tag)