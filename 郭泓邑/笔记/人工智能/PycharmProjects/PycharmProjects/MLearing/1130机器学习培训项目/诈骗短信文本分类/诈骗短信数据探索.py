# 导入必要的库
import re
from collections import Counter

import jieba
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from wordcloud import WordCloud
warnings.filterwarnings('ignore')
# 设置中文字体和图形样式
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
#加载用户字典
jieba.load_userdict("data_set/user_dict.txt")
#加载停用词表
with open("data_set/stop_words.txt","r",encoding="utf-8") as fr:
    stop_words = fr.read().split("\n")


scam_words =[]
non_scam_words =[]
def words_extract(text,scam=True):
    # 使用正则表达式剔除文本中的非中文字符 [^\u4e00-\u9fa5] 固定代码格式
    text = re.sub(r"[^\u4e00-\u9fa5]", "", text)
    # 使用jieba进行分词并过滤停用词
    fliter_words = [wd for wd in jieba.lcut(text)
                    if wd not in stop_words and len(wd) > 1]
    #  保存分词结果
    if scam:
        scam_words.extend(fliter_words)
    else:
        non_scam_words.extend(fliter_words)
# end scam_words_extract(text)

# 可视化分析结果
def plot_result(scam_top_10_words, scam_words,
                non_scam_top_10_words,non_scam_words):
    plt.figure(figsize=(12, 5))
    # 绘制2行2列中的第1个子图
    plt.subplot(2, 2, 1)
    # 绘制柱状图
    plt.bar( list(scam_top_10_words.keys()),
           list(scam_top_10_words.values()),
           align='center')
    # 绘制柱状图的值
    for i, v in enumerate(scam_top_10_words.values()):
        plt.text(i, v+1, v, ha='center', va='bottom')
    plt.title("诈骗短信分词结果")
    #x轴坐标倾斜30度
    plt.xticks(rotation=30)
    plt.ylabel("词频")
    plt.grid(axis='y')

    # 绘制词云
    plt.subplot(2, 2, 2)
    #前置操作 读入词云的背景图片
    #7.1 需要创建绘制词云的对象
    wc = WordCloud(
        font_path="C:\Windows\Fonts\SimHei.ttf",#加入系统的字体库
        width=600,#词云画布的宽
        height=300,#词云画布的高
        max_words=500,#最多显示500个词
        background_color='white'#设置背景色
    )
    #加载统计好的词频
    wc.generate_from_frequencies(scam_words)
    #显示图像
    plt.imshow(wc, interpolation='bilinear' #使得图片平滑
               )
    plt.title("诈骗短信词云")
    plt.axis("off")
    plt.tight_layout()
    # 绘制2行2列中的第3个子图
    plt.subplot(2, 2, 3)
    # 绘制柱状图
    plt.bar(list(non_scam_top_10_words.keys()),
            list(non_scam_top_10_words.values()),
            align='center')
    # 绘制柱状图的值
    for i, v in enumerate(non_scam_top_10_words.values()):
        plt.text(i, v + 1, v, ha='center', va='bottom')
    plt.title("非诈骗短信分词结果")
    # x轴坐标倾斜30度
    plt.xticks(rotation=30)
    plt.ylabel("词频")
    plt.grid(axis='y')

    # 绘制词云
    plt.subplot(2, 2, 4)
    # 前置操作 读入词云的背景图片
    # 7.1 需要创建绘制词云的对象
    wc = WordCloud(
        font_path="C:\Windows\Fonts\SimHei.ttf",  # 加入系统的字体库
        width=600,  # 词云画布的宽
        height=300,  # 词云画布的高
        max_words=500,  # 最多显示500个词
        background_color='white'  # 设置背景色
    )
    # 加载统计好的词频
    wc.generate_from_frequencies(non_scam_words)
    # 显示图像
    plt.imshow(wc, interpolation='bilinear'  # 使得图片平滑
               )
    plt.title("非诈骗短信词云")
    # 图片显示边框，不显示坐标
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("诈骗数据探索分析.jpg")
    plt.show()

#end plot_result



if __name__ == '__main__':
    # 读取数据
    df = pd.read_csv('data_set/Scam_text_message.csv')
    # 处理诈骗的数据
    df[df["target"] == "诈骗"]["content"].apply(lambda text: words_extract(text))
    print(scam_words)
    scam_words_count = Counter(scam_words)
    print(scam_words_count)
    # 提取10个高频涉及到诈骗的词
    scam_top_10_words = scam_words_count.most_common(10)
    # 将结果转换成字典
    scam_top_10_words = dict(scam_top_10_words)

    # 非诈骗数据信息的处理
    df[df["target"] == "非诈骗"]["content"].apply(lambda text: words_extract(text,scam=False))
    print(non_scam_words)
    non_scam_words_count = Counter(non_scam_words)
    print(non_scam_words_count)
    # 提取10个高频涉及到非诈骗的词
    non_scam_top_10_words = non_scam_words_count.most_common(10)
    # 将结果转换成字典
    non_scam_top_10_words = dict(non_scam_top_10_words)

    # 调用可视化的函数进行分析结果的展示
    plot_result(scam_top_10_words,scam_words_count,non_scam_top_10_words,non_scam_words_count)