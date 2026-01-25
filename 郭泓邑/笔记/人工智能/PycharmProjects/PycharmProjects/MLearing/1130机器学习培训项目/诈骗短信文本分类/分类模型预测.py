import re
import jieba
import joblib
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

def scam_msg_predict(text):
    try:
        # 加载模型
        model = joblib.load('train_model/sms_classifier.pkl')
        # 进行预测
        prediction = model.predict([text])[0]
        proba = model.predict_proba([text])[0]
        # 返回结果
        result = {
            'text': text,
            'prediction': prediction,
            'probability': {
                '诈骗概率': round(proba[0] * 100, 2),
                '非诈骗概率': round(proba[1] * 100, 2)
            }
        }
        return result
    except Exception as e:
        return {'error': str(e)}


if __name__ == '__main__':
    test_messages = [
        "航旅纵横：您预订的9C8888航班值机已开放，可手机选座",
        "【共享屏幕】您的银行APP操作被录屏！转账3万元删除记录：http://screen-hack.net",
        "恭喜您获得大奖，点击链接领取",
        "您的快递已到达小区快递柜",
    ]

    for msg in test_messages:
        result = scam_msg_predict(msg)
        print(f"文本: {result['text']}")
        print(f"预测结果: {result['prediction']}")
        print(f"概率: 诈骗 {result['probability']['诈骗概率']}%, "
              f"非诈骗 {result['probability']['非诈骗概率']}%")
        print("-" * 50)