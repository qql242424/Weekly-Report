import time
import pandas as pd
from snownlp import SnowNLP
import re


def analyze_sentiment(text):
    clean_text = re.sub("[^\u4e00-\u9fa5]", "", text)
    s = SnowNLP(clean_text)
    _score = s.sentiments
    if _score <= 0.3:
        return '消极情感'
    elif _score <= 0.7:
        return '中性情感'
    else:
        return '积极情感'
# end analyze_sentiment

if __name__ == '__main__':
    print("加载数据")
    df = pd.read_csv("data_set/comment_data.csv")
    print("情感数据标注中.....")
    df.loc[:,"sentiment_category"] = df["comment"].apply(lambda text:analyze_sentiment(text))
    time.sleep(2)
    print("数据文件标注完成,正在保存中......")
    df.to_csv("data_set/comment_data_tag.csv"
              ,encoding="utf-8"
              ,header=True
              ,index=False)