import pymysql
import jieba
from collections import Counter
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud


def coon():  # 连接数据库
    con = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='movies',
                          charset='utf8')  # 连接数据库
    cur = con.cursor()
    return con, cur


def close():
    con, cur = coon()  # 关闭数据库
    cur.close()
    con.close()


def qurey(sql):
    con, cur = coon()  # 查询数据库
    cur.execute(sql)
    res = cur.fetchall()
    close()
    return res


def insert(sql):
    con, cur = coon()  # 删除数据库表
    cur.execute(sql)
    con.commit()
    close()


def LDA(text):
    jiebaword = []
    for line in text:
        line = line.strip('\n')
        # 清除多余的空格
        line = "".join(line.split())
        # 默认精确模式
        seg_list = jieba.cut(line, cut_all=False)
        word = "/".join(seg_list)
        jiebaword.append(word)
    stopwords_filepath = "./static/stopwords.txt"
    # 读取停用词表
    stopwords = [line.strip() for line in open(stopwords_filepath, 'r', encoding='utf-8').readlines()]
    stopwords.append('##')
    fw = open('./static/clean.txt', 'w', encoding='utf-8')
    # 去除停用词
    word3 = ''
    for words in jiebaword:
        words = words.split('/')
        for word in words:
            if word not in stopwords:
                word3 += word + " "
                fw.write(word + '\t')
        fw.write('\n')
    fw.close()
    with open('./static/clean.txt', "r", encoding='utf-8') as fr:
        wordList = fr.readlines()
    # 生成tfidf矩阵
    transformer = TfidfVectorizer()
    tfidf = transformer.fit_transform(wordList)
    # 转为数组形式
    tfidf_arr = tfidf.toarray()
    km = nltk.cluster.kmeans.KMeansClusterer(num_means=3, distance=nltk.cluster.util.cosine_distance)
    # 进行kmeans聚类分析
    km.cluster(tfidf_arr)
    data0 = []
    data1 = []
    data2 = []
    for data, word in zip(tfidf_arr, wordList):
        if km.classify(data) == 0:
            word = word.replace('\n', '').split('\t')
            for i in word:
                if i != "":
                    data0.append(i)
        elif km.classify(data) == 1:
            word = word.replace('\n', '').split('\t')
            for i in word:
                if i != "":
                    data1.append(i)
        elif km.classify(data) == 2:
            word = word.replace('\n', '').split('\t')
            for i in word:
                if i != "":
                    data2.append(i)
    data = data0 + data1 + data2
    data = Counter(data)
    d2 = sorted(data.items(), key=(lambda x: x[1]), reverse=True)
    data = []
    for i in d2[:4]:
        data.append(list(i))
    return data


def wordcloud(text):
    jiebaword = []
    for line in text:
        line = line.strip('\n')
        # 清除多余的空格
        line = "".join(line.split())
        # 默认精确模式
        seg_list = jieba.cut(line, cut_all=False)
        word = "/".join(seg_list)
        jiebaword.append(word)
    stopwords_filepath = "./static/stopwords.txt"
    # 读取停用词表
    stopwords = [line.strip() for line in open(stopwords_filepath, 'r', encoding='utf-8').readlines()]
    stopwords.append('##')
    fw = open('./static/clean.txt', 'w', encoding='utf-8')
    # 去除停用词
    word3 = ''
    for words in jiebaword:
        words = words.split('/')
        for word in words:
            if word not in stopwords:
                word3 += word + " "
                fw.write(word + '\t')
        fw.write('\n')
    fw.close()
    with open('./static/clean.txt', "r", encoding='utf-8') as fr:
        wordList = fr.readlines()
    # 生成词云图
    my_wordcloud = WordCloud(background_color=("#fff"), font_path="C:\Windows\Fonts\simhei.ttf", scale=4).generate(
        word3)  # 注：song.ttc  设置展示的图文的字体
    my_wordcloud.to_file("./static/images/result.png")  # 保存图片