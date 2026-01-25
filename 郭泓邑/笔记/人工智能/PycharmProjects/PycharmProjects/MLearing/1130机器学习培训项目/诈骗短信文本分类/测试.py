import jieba
jieba.load_userdict("data_set/user_dict.txt")
text="河北建材职业技术学院，中国移动"
print(jieba.lcut(text))