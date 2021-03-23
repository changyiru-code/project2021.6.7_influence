# #读取mongodb数据库，存到result_list列表，该列表里存放字典，一个字典代表一条数据
# input: result_list  [{'id':1,'zan':222,...},{'id':2,'zan':22,...},...]
# output: [[{'id':1,'zan':222,...},{'id':2,'zan':22,...},...], [{'id':1,'zan':222,...},{'id':2,'zan':22,...},...], [{'id':1,'zan':222,...},{'id':2,'zan':22,...},...],...]
# 分析：先将带有HashTag的文本筛选出来，内容只留下HashTag值，以及需要的字段
# 'repostsCount', 'commentsCount', 'createAt'，接着对HashTag的文本分词、向量化、加权、计算余弦相似度、单遍聚类，得到输出


# 导包
from pymongo import MongoClient
import pandas as pd
import numpy as np
from datetime import datetime
import copy
import re
import jieba
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import word2vec


def is_chinese(uchar):
    if uchar>=u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False


def fenci(document):
    # 分词
    cut_words = jieba.cut(document)
    contents = list(cut_words)
    # 去停用词
    stpwrdpath = '哈工大停用词表.txt'
    stpwrd_dic = open(stpwrdpath, 'r', encoding='utf-8')
    stpwrd_content = stpwrd_dic.read()
    stopwords = stpwrd_content.splitlines()  # 加载停用词表
    # print(list(cut_words))
    contents_clean = []
    for word in contents:
        if word in stopwords:
            continue
        contents_clean.append(word)
    # print(contents_clean)
    # 去掉文本中的空格
    document_qukongge = []
    for list_word in contents_clean:
        m1 = list_word.replace(' ', '')
        document_qukongge.append(list(m1))  # 调用qukongge()函数
    # print(document_qukongge)
    # 让文本只保留汉字
    chinese_list = []
    for content in document_qukongge:
        content_list = []
        content_str = ''
        for word in content:
            if is_chinese(word):
                content_str = content_str + word
        content_list.append(content_str)
        chinese_list.append(content_list)
    # print(chinese_list)
    # 去掉空字符
    document_qukong = []
    for line in chinese_list:
        qukong_list = []
        for j in line:
            if j == '':
                continue
            else:
                qukong_list.append(j)
        document_qukong.append(qukong_list)
    # print(document_qukong)  # 去空后的分词结果
    # #移除空列表
    list_document = []
    for line in document_qukong:
        if line:
            list_document.append(line)
    # print(list_document)
    document_result = []
    for line in list_document:
        document_result1 = ' '.join(line)
        document_result.append(document_result1)
    # print(document_result)
    # 变为字符串
    list_result = ' '.join(document_result)
    return list_result


# 文本tf-idf处理
def tfidf(text,model):
    vector = TfidfVectorizer()
    tfidf = vector.fit_transform(text)
    tfidf_all_word = vector.get_feature_names()
    # print(tfidf_all_word)  # 显示所有文本的词汇，列表类型
    tfidf_dict = vector.vocabulary_
    # print(tfidf_dict)  # 词汇表，字典类型，每个词都有一个索引id
    tfidf_todense = tfidf.todense()  # 将稀疏矩阵转为完整特殊矩阵
    tfidf_array = tfidf_todense.A   # 将矩阵转为数组
    # print(tfidf_array)
    zhengwen_list = []
    for line in text:  #'盖茨 特朗普 警告 流行病 后悔 加大 推进 力度'
        line_list = line.split(' ')
        zhengwen_list.append(line_list)
    # print(zhengwen_list) #[['盖茨', '特朗普', '警告', '流行病', '后悔', '加大', '推进', '力度'], ['数万', '知乎', '网友', '自荐', '看到', '浑身', '颤抖', '无法自拔', '久久不忘', '电影', '入选', '影片', '豆瓣', '评分', '欢迎', '补充', '心目', '电影']]
    m = 0
    wenben_vector = []
    for list in zhengwen_list:
        # print(list)
        feature_vec = np.zeros((100,), dtype='float32')
        for word in list:
            if word in tfidf_all_word:
                i = tfidf_dict[word]
                tfidf = tfidf_array[m][i]
                vector = model.wv[word]
                # print(vector)
                tfidf_vector = vector * tfidf
                # print(word, tfidf_vector)

                feature_vec = np.add(feature_vec, tfidf_vector)
            else:
                continue
        wenben_vector.append(feature_vec)
        m = m + 1
    # print(wenben_vector)
    wenben_array = np.array(wenben_vector)  # 将列表转为数组
    print(type(wenben_array))
    return wenben_array
    # np.save("yanshi_vector.npy", wenben_array.reshape(len, 100))#将文本权值向量保存在yanshi_vector.npy中


def get_similary(vector_1, vectors_2):#余弦相似性
    norm = np.linalg.norm(vector_1)
    all_norms = np.linalg.norm(vectors_2)
    dot_products = np.dot(vectors_2, vector_1)
    simi = dot_products / (norm * all_norms)
    return simi


def get_max_similarity(cluster_cores, vector):
    max_value = 0
    max_index = -1
    for k, core in cluster_cores.items():
        similarity = get_similary(vector, core)
        if similarity > max_value:
            max_value = similarity
            max_index = k
    return max_index, max_value


#单遍聚类
def single_pass(corpus_vec, corpus, theta):
    clusters = {}  #存放聚类结果,键是话题数，值是话题里的文本的向量
    cluster_cores = {}   #质心向量，话题中心，用clusters里的向量来求
    cluster_text = {}    #存放聚类结果,键是话题数，值是话题里的文本
    num_topic = 0   #定义一个话题数
    for vector, text in zip(corpus_vec, corpus): #序列解包，同时遍历corpus_vec和corpus，
        if num_topic == 0:                       # 分别赋给vector和text
            clusters.setdefault(num_topic, []).append(vector)
            cluster_cores[num_topic] = vector
            cluster_text.setdefault(num_topic, []).append(text)
            num_topic += 1
        else:
            max_index, max_value = get_max_similarity(cluster_cores, vector)
            if max_value > theta:
                clusters[max_index].append(vector)
                text_list = clusters[max_index]   #text_list是一个列表类型<class 'list'>
                text_matrix = np.mat(text_list)   #将列表转为矩阵类型，以求算数平均值
                core = np.mean(text_matrix, axis=0)  # 更新簇中心,求质心向量
                core = core.A   #将矩阵转为数组类型
                cluster_cores[max_index] = core[0]
                cluster_text[max_index].append(text)
            else:  # 创建一个新簇
                clusters.setdefault(num_topic, []).append(vector)
                cluster_cores[num_topic] = vector
                cluster_text.setdefault(num_topic, []).append(text)
                num_topic += 1
    return clusters, cluster_text


def extract_hashtag(data):
    # 1、提取每个文本内容的hashtag
    df1 = pd.DataFrame(data)  # 读取集合的全部数据
    df2 = df1['repostsCount'].tolist()  # 只提取转发
    df3 = df1['commentsCount'].tolist()  # 只提取评论
    df4 = df1['createAt'].tolist()  # 只提取发表时间  df3数据类型<class 'pandas.core.series.Series'>
    df5 = df1['content'].tolist()  # 只提取正文内容
    content_list1 = []
    for str in df5:
        pattern = re.compile('#(.+)#')  # 匹配从#开始，到#结束的内容
        result = pattern.findall(str)
        content_list1.append(result)      # content_list1存放全部的内容
    # print(content_list1)

    # 2、获取带有hashtag的内容及对应的转发、评论和时间
    result_list1 = []
    for index, value in enumerate(content_list1):
        result_dict = {}
        if value:        # 判断列表result是否为空，空代表没有hashtag,则删掉
            result_dict['content'] = value[0]
            result_dict['repostsCount'] = df2[index]
            result_dict['commentsCount'] = df3[index]
            result_dict['createAt'] = df4[index]
            result_list1.append(result_dict)   # result_list1存放带有hashtag的内容及对应的转发、评论和时间
    # print(result_list1)  # [{'content': '昊嘉青易# #赖小民一审被判死刑', 'repostsCount': 0, 'commentsCount': 0, 'createAt': '2021-01-09 22:23:30'},{...},,,]
    result_list2 = copy.deepcopy(result_list1)
    # 对HashTag的文本分词
    for content_dict1 in result_list1:
        list_result = fenci(content_dict1['content'])
        content_dict1['content'] = list_result
    # print(result_list1)  # [{'content': '昊嘉青易 赖 小民 一审 被判 死刑', 'repostsCount': 0, 'commentsCount': 0, 'createAt': '2021-01-09 22:23:30'}, {...}]
    # 只读取content
    fenci_list=[]   # 这个列表里放全部的分词，用来做词向量化
    for content_dict2 in result_list1:
        fenci_list.append(content_dict2['content'])
    # print(fenci_list)  # ['昊嘉青易 赖 小民 一审 被判 死刑', '赖 小民 一审 被判 死刑',...]
    list1_str = ' '.join(fenci_list)
    sentences = [list1_str.split(' ')]   # [['昊嘉青易', '赖', '小民', '一审',...]]
    # 训练词向量
    model = Word2Vec(sentences, sg=1, hs=1, min_count=1, window=3, size=100)
    print(model.wv.index2word)
    print(model)
    corpus_vec = tfidf(fenci_list, model)  # ,len(fenci_list)
    clusters, cluster_text = single_pass(corpus_vec, result_list1, 0.85)
    print(cluster_text)

# 创建连接MongoDB数据库函数
def connection():
    # 1:账号密码方式连接本地MongoDB数据库服务 | "mongodb://用户名:密码@公网ip:端口/"
    conn = MongoClient("mongodb://root:19980529@127.0.0.1:27017/")  # 用户名、密码可修改
    # 2:连接本地数据库(influence)和集合
    collection = conn["influence"]["keyword6_status"]
    data = collection.find()
    data = list(data)  # 在转换成列表时，可以根据情况只过滤出需要的数据。(for遍历过滤)

    extract_hashtag(data)


# 创建主函数
def main():
    connection()


main()
