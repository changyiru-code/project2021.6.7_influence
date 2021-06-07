# # 读取mongodb数据库，只读取一个事件，时间以时为单位（话题持续多少小时），运行公式模型，计算单独一个事件的影响力，输出结果格式为字典，进行归一化
# 读取数据库里的测试数据，验证模型
# 存入数据库
"""
该代码将一个事件内的文章聚类出多个话题
"""
"""
2021.6.7 19:27代码已完成计算事件的多个话题的影响力，并提取到每个话题的名字
"""
# 导包
from pymongo import MongoClient
import pandas as pd
import numpy as np
from datetime import datetime
import json
import requests
import logging
import threading
import re
import copy
import jieba
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
import time
from flask import Flask, request, jsonify
app = Flask(__name__)
app.debug = True
from gevent import pywsgi
logging.basicConfig(level=logging.DEBUG)  # jia

# 计算时间差的函数
def timecha(time1, time2):
    diff_day = (time1 - time2).days
    diff_sec = (time1 - time2).seconds
    m, s = divmod(diff_sec, 60)  # 时间差是diff_day天h时m分s秒
    h, m = divmod(m, 60)
    h_cha = diff_day * 24 + h   # 时间差，以时为单位
    if (h == 0 and (m != 0 or s != 0)) or m > 30:
        T = h_cha + 1   # 如果时间差超过12小时，则按一天算，不足12时不按一天算
    else:
        T = h_cha
    return T


# 将各评价指标结果归一化
def normalize(count_result):
    func = lambda x: np.exp(x)
    result = map(func, count_result)
    exp_count_result = [e_result+1 for e_result in list(result)]  # exp()  先对结果求指数 先对结果求指数,但是求对数以后还可能处于0-1之间，所以下面取对数就变成了负值

    func = lambda x: np.log(x)/np.log(max(exp_count_result))
    result = map(func, exp_count_result)
    norm_result = list(result)  # ln(x)/ln(max) 话题各指标归一化，范围[0,1]

    norm_result = [i * 100 for i in norm_result]
    return norm_result    # 乘以100，得到范围[0,100]


# 定义熵值法函数
def cal_weight(x):
    '''熵值法计算变量的权重'''
    fenshu = copy.deepcopy(x)
    # 标准化
    fenshu = fenshu.apply(lambda fenshu: ((fenshu - np.min(fenshu)) / (np.max(fenshu) - np.min(fenshu))))
    # 求k
    rows = fenshu.index.size  # 行
    k = 1.0 / np.log(rows)
    yij = (1 + fenshu).sum(axis=0)
    # 第二步，计算pij
    pij = (1 + fenshu) / yij
    test = pij * np.log(pij)
    test = np.nan_to_num(test)
    # 计算每种指标的信息熵
    ej = -k * (test.sum(axis=0))
    # 计算每种指标的权重
    w = (1 - ej) / np.sum(1 - ej)
    add_wi = x * w
    score = add_wi.sum(axis=1)
    score = score.tolist()
    score_li = []
    for i_score in score:
        if i_score == 0:
            i_score += 0.1
        score_li.append(i_score)
    return score_li


# 读取事件集合，获得转发，评论数；微博文章数；持续时间；时间单元数差；爬虫起止时间
def event_influ_calcu(cluster_text, topicId, content_topic):
    # 1:读取数据集的每一个话题数据，计算每个话题的所需内容
    # 读取数据库，获得转发，评论数；微博文章数；持续时间；时间单元数差；爬虫起止时间
    li_all = []  # 存放每个话题的全部转发，评论数
    li_count = []  # 存放每个话题里的微博文章数Mj
    li_T = []  # 话题持续时间Tj
    li_dt = []  # 当前时间与话题首次发布时间的时间单元数差det(tj)
    li_starttime = []  # 每个事件的开始时间
    li_endtime = []  # 每个事件的结束时间
    data_list = []  # 列表，[[{},{},...], [{},{},...], [{},{},...]]
    for li_i in range(len(cluster_text)):
        data_list.append(cluster_text[li_i])
    print(data_list)
    for data in data_list:
        # 1读取数据
        logging.info("读取数据")  # jia1
        df1 = pd.DataFrame(data)  # 读取集合的全部数据
        df2 = df1[['repostsCount', 'commentsCount']]  # 只提取转发和评论
        ylist_sum = df2.sum(axis=0)
        li_ylist_sum = ylist_sum.values.tolist()  # 将dataframe类型的值转换成列表
        li = []
        li.extend(li_ylist_sum)
        li_all.append(li)

        logging.info("求事件的文章个数Mj")  # jia1
        # 2求每个话题的文章个数Mj
        rows = df1.index.size  # 行数
        li_count.append(rows)

        logging.info("求每个话题的持续时间Tj")  # jia1
        # 3求每个话题的持续时间Tj
        mod_times = df1['createdAt']  # 提取每一行的时间
        mod_times = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x / 1000)) for x in
                     mod_times]  # gai1 时间戳转换为格式化字符串
        mod_times = [datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in mod_times]  # 改str类型为datetime.datetime类型
        max_time = max(mod_times)  # 该话题的结束时间
        min_time = min(mod_times)  # 该话题的开始时间
        T = timecha(max_time, min_time)  # 该话题的持续时间
        if T == 0:
            li_T.append(T + 0.1)
        else:
            li_T.append(T)
        # 4定义爬虫的起止时间
        li_starttime.append(min_time)
        li_endtime.append(max_time)

        logging.info("获取当地时间")  # jia1
        # 5获取当地时间,格式化成2016-03-20 11:45:39形式,获得当前时间与话题首次发布时间的时间单元数差
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当地时间
        now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')  # 改str类型为datetime.datetime类型
        dt = timecha(now, min_time)
        li_dt.append(dt)

    # 计算爬虫的起止时间
    end_time = max(li_endtime)  # 每个事件结束时间的最大值，得到爬虫的结束时间
    start_time = min(li_starttime)  # 每个事件开始时间的最小值，得到爬虫的开始时间
    n_dt = timecha(end_time, start_time)  # 爬虫的起止时间

    M = sum(li_count)

    logging.info("计算公式中的各个指标")  # jia1

    # 2:计算公式中的各个指标
    func = lambda x: np.exp(x / M)
    result = map(func, li_count)
    count_result = list(result)  # exp(Mj/M)  计算话题覆盖度
    norm_cover_result = normalize(count_result)  # 归一化覆盖度值
    print(norm_cover_result)

    func1 = lambda x, y: np.log(x / y)
    result = map(func1, li_count, li_T)
    li_count_result = list(result)  # ln(Mj/Tj) 计算话题活跃度
    norm_activity_result = normalize(li_count_result)  # 归一化活跃度值
    print(norm_activity_result)

    func2 = lambda x: 1 / (np.power(x, 0.1))  # 也可以将0.1改成0.5，参考论文是0.5
    result = map(func2, li_dt)
    li_dt_result = list(result)  # (dt+1)^-0.1 计算话题新颖度
    norm_novelty_result = normalize(li_dt_result)  # 归一化新颖度值
    print(norm_novelty_result)

    func3 = lambda x: x / n_dt
    result = map(func3, li_T)
    n_result = list(result)  # nu/n  计算话题持久度
    norm_persist_result = normalize(n_result)  # 归一化持久度值
    print(norm_persist_result)

    # 计算用户参与度
    # 读取li_all的转发数和评论数，利用熵权法计算每个话题转发，评论对话题影响力的贡献值
    # 1读取数据
    repose_comment = pd.DataFrame(li_all, columns=['该话题总转发数', '该话题总评论数'])
    # 2数据预处理 ,去除空值的记录
    repose_comment.dropna()
    score = cal_weight(repose_comment)  # 计算用户参与度
    print(score)
    # 用户参与度归一化
    func4 = lambda x: np.log(x)/np.log(max(score))
    result = map(func4, score)
    norm_score_result = list(result)  # ln(x)/ln(max)
    user_engage = [i * 100 for i in norm_score_result]   # 用户参与度归一化,乘以100
    print(user_engage)

    logging.info("计算总公式")  # jia1

    # 3:计算总公式  话题影响力值
    dict1 = {}   # 存放最后的结果，字典形式
    list1 = []    # 存放每个话题各评价指标及总影响力值，列表形式
    func = lambda x: np.exp(x)
    result = map(func, li_count_result)
    li_count_result = list(result)
    influence = [score[i] * li_count_result[i] * count_result[i] * n_result[i] * li_dt_result[i] for i in range(len(score))]  # 总公式  话题影响力值
    print(influence)
    # 话题影响力总值归一化
    func5 = lambda x: np.log(x)/np.log(max(influence))
    result = map(func5, influence)
    norm_influ_result = list(result)  # ln(x)/ln(max) 话题影响力归一化
    norm_influ_result = [i * 100 for i in norm_influ_result]  # l话题影响力归一化,乘以100

    logging.info("将每个话题的对应结果存入列表")  # jia1
    # 4:将每个话题的对应结果存入列表
    dict1["case_id"] = topicId
    for i in range(len(norm_influ_result)):
        dict2 = {}
        dict2["topic"] = content_topic[i]
        dict2["topic_influence"] = norm_influ_result[i]
        dict2["user_engage"] = user_engage[i]
        dict2["topic_coverage"] = norm_cover_result[i]
        dict2["topic_activity"] = norm_activity_result[i]
        dict2["topic_novelty"] = norm_novelty_result[i]
        dict2["topic_persistence"] = norm_persist_result[i]
        list1.append(dict2)    # list1是字典格
    list1 = sorted(list1, key=lambda list1: list1["topic_influence"], reverse=True)
    print("降序后列表:{}".format(list1))
    dict1["result"] = list1    # list1是字典格式
    return dict1


def save_to_db(dict1, topicId):
    logging.info("连接数据库...")  # jia
    try:   # jia
        # # 1:账号密码方式连接本地MongoDB数据库服务 | "mongodb://用户名:密码@公网ip:端口/"
        # conn = MongoClient("mongodb://SOCIAL_ATTENTION:EF_KD_BJD-!24@10.20.2.181:28018/")  # 用户名、密码可修改
        # # 2:连接本地分析结果数据库(SOCIAL_ATTENTION)和集合(social_influence)
        # db = conn["SOCIAL_ATTENTION"]["social_influence"]

        # 数据库有密码认证的话要用下面的连接方式
        conn = MongoClient("mongodb://10.20.2.181:28018/")
        mydb = conn["SOCIAL_ATTENTION"]  # SOCIAL_ATTENTION是数据库名称
        mydb.authenticate('SOCIAL_ATTENTION', 'EF_KD_BJD-!24')
        db = mydb["social_influence"]  # social_influence是数据库的中一个数据表


        logging.info("数据库连接成功")  # jia
        # db.delete_many({})
        # db.insert_one(dict1)
        db.update_one(
            {'case_id': topicId},
            {'$set':
                 dict1
             },
            upsert=True
        )
        return "SOCIAL_ATTENTION", "social_influence"
    except Exception as e:   # jia
        logging.error("数据库连接失败：%s" % e)   # jia

    # 5：消息服务接口,通知计算完成，给出存数据的数据库名和集合名，
def send_message_api(eventNoticeType, eventState, db_name, collection_name, topicId):  # jia2 eventNoticeType:通知消息类型说明,值为SOCIAL_INFLUENCE表示社会影响力效能评估；eventState：消息服务状态说明，值为SUCCESSFUL表示执行成功并已完成
    BasePath = 'https://api.antdu.com/event/'
    url = BasePath+'notice'
    logging.info("消息服务接口链接: %s", url)  # jia
    # 消息头指定,指定utf-8编码
    # headers = {'Content-Type': 'application/json;charset=UTF-8'}
    data = {'noticeType': eventNoticeType, 'eventState': eventState, 'db_name': db_name, 'collection_name': collection_name, 'topicId': topicId}
    try:  # jia
        r = requests.post(url, data=data)
        print(r.text)
        logging.info("成功通知消息服务接口：%s", r.text)  # jia
    except Exception as e:    # jia
        logging.error("通知消息服务接口失败：%s" % e)  # jia


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
    s = norm * all_norms
    if s == 0:
        simi = 0.0
    else:
        simi = dot_products / s
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
    df4 = df1['createdAt'].tolist()  # 只提取发表时间  df3数据类型<class 'pandas.core.series.Series'>
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
            result_dict['createdAt'] = df4[index]
            result_list1.append(result_dict)   # result_list1存放带有hashtag的内容及对应的转发、评论和时间
    # print(result_list1)  # [{'content': '昊嘉青易# #赖小民一审被判死刑', 'repostsCount': 0, 'commentsCount': 0, 'createAt': '2021-01-09 22:23:30'},{...},,,]
    # result_list2 = copy.deepcopy(result_list1)
    # 对HashTag的文本分词
    fenci_list=[]   # 这个列表里放全部的分词，用来做词向量化
    for content_dict1 in result_list1:
        list_result = fenci(content_dict1['content'])
        fenci_list.append(list_result)
    # print(result_list1)  # [{'content': '昊嘉青易 赖 小民 一审 被判 死刑', 'repostsCount': 0, 'commentsCount': 0, 'createAt': '2021-01-09 22:23:30'}, {...}]
    # print(fenci_list)  # ['昊嘉青易 赖 小民 一审 被判 死刑', '赖 小民 一审 被判 死刑',...]
    list1_str = ' '.join(fenci_list)
    sentences = [list1_str.split(' ')]   # [['昊嘉青易', '赖', '小民', '一审',...]]
    # 训练词向量
    model = Word2Vec(sentences, sg=1, hs=1, min_count=1, window=3, size=100)
    print(model.wv.index2word)
    print(model)
    corpus_vec = tfidf(fenci_list, model)  # ,len(fenci_list)

    clusters, cluster_text = single_pass(corpus_vec, result_list1, 0.80)
    print(cluster_text)    # 最终聚类结果

    # 以下几行需添加, 为了得到话题名称
    content_topic = []
    for p in list(cluster_text.values()):
        content_1 = [i['content'] for i in p]
        print(content_1)
        maxtag = max(content_1, key=content_1.count)
        print(maxtag)
        content_topic.append(maxtag)
    print(content_topic)

    return cluster_text, content_topic


# 通过ID读数据库数据
# 2：连接数据库，得到集合数据，数据库访问接口，要改接口
# 收到通知后，以事件id作为参数调用提供的一个事件关联数据查询接口翻页查询事件关联的数据进行事件影响力分析。
# 怎么通过id访问，目前是通过数据库名和集合名读取数据
# 通过ID读数据库数据
def getdata_fromdb_by_id(topicId):
    logging.info('成功调用读数据库函数')  # jia
    BasePath = 'https://api.antdu.com/jw/'
    url = BasePath + 'data/documents'   # https://api.antdu.com/jw/data/documents
    logging.info('输出数据库接口链接: %s', url)  # jia
    endTime = int(round(time.time() * 1000))  # jia1
    startTime = 0   # jia1,endTime-86700，86400是往前一天，为避免前面调数据有时延，时间往前5分钟
    print(endTime)
    # startTime = 161509171800
    # endTime = 1615523719551  # 这两个时间是测试时间

    data = {"topic": topicId, 'startTime': startTime, "endTime": endTime, "count": 100}  # jia1
    logging.info('向数据库发送请求获取数据')  # jia
    # 向数据库发送请求获取数据
    try:
        c = 1  # jia

        requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接

        data = requests.get(url, params=data)
        data = json.loads(data.text)  # gai1
        logging.info("数据库第 %s 次请求成功", c)  # jia
        # logging.info("数据库第 %s 次请求得到的数据", data)  # shan1
        numFound = data["numFound"]  # 事件数据库里一共有这么多条数据，根据该数据判断要读多少次
        print(numFound)
        result_list = data["result"]  # 该列表里存放字典，一个字典代表一条数据
        endTime = result_list[-1]["createdAt"]
        count = 100
        print("endTime: ", endTime)  # jia1
        logging.info("数据库本次请求得到数据")  # jia1
        for i in range(int(numFound / count)):  # 读事件库的全部数据存到result_list列表里
            c += 1  # jia
            data2 = {"topic": topicId, 'startTime': startTime, "endTime": endTime, "count": count}  # gai1
            data2 = requests.get(url, params=data2)
            data2 = json.loads(data2.text)  # gai1
            logging.info("数据库第 %s 次请求成功", c)  # gai1
            logging.info("数据库本次请求得到数据")  # gai1

            result_list = result_list + data2["result"][1:]  # gai1,该列表里存放字典，一个字典代表一条数据
            endTime = result_list[-1]["createdAt"]
        print(len(result_list))  # jia1
        logging.info("数据库数据读取完毕,接下来是影响力计算")  # jia

        # 2.5: 根据hashtag聚类,得到一个事件下的多个话题
        cluster_text, content_topic = extract_hashtag(result_list)

        # 3：影响力计算
        dict1 = event_influ_calcu(cluster_text, topicId, content_topic)
        logging.info("影响力计算结束，数据输出")  # gai1
        print(dict1)

        # 4：将计算结果存入数据库
        logging.info("数据准备存入数据库...")  # jia
        db_name, collection_name = save_to_db(dict1, topicId)
        logging.info("数据已全部存入数据库,准备连接并通知消息服务，计算完成")  # jia

        # 5：消息服务接口,通知计算完成,给出存数据的数据库名和集合名:接口
        send_message_api('SOCIAL_INFLUENCE', 'SUCCESSFUL', db_name, collection_name, topicId)  # jia2

    except Exception as e:
        logging.error("数据库请求异常：%s" % e)  # gai
        # data = None
        # return data


# 1、消息服务接口,接收数据导入成功的通知
# 接收消息
@app.route('/notice', methods=['post'])  # url = 'http://127.0.0.1:8088/notice',请求方式post
def add_stu():
    try:  # jia
        logging.info('接口被调用成功')  # jia
        logging.info('接收到的数据：%s', request.values)    # jia
        # 获取通过url请求传参的数据
        eventState = request.values.get('eventState')
        topicId = request.values.get('topicId')
        # 判断状态、类型、id都不为空
        if eventState and topicId:
            if eventState == 'SUCCESSFUL':
                logging.info('调用读数据库函数')  # jia
                getdata_fromdb_by_id(topicId)  # 如果接收到 数据全部入库 的消息，则根据通知接口拿到的事件ID（topicId）去调用接口3.2.1.3，获取我们需要的数据
                return 'true'
            else:
                logging.info('发送的消息不对')  # jia
                resu = {'code': -1, 'message': '类型或状态不对'}
                return json.dumps(resu, ensure_ascii=False)
        else:
            resu = {'code': 10001, 'message': '未检测到数据or参数不能为空！'}
            return json.dumps(resu, ensure_ascii=False)
        # 返回JSON数据。
    except Exception as e:  # jia
        logging.error("接口被调用失败：%s" % e)  # jia


# 创建主函数
if __name__ == '__main__':
    # 1：消息服务接口,接收数据导入成功的通知:接口
    server = pywsgi.WSGIServer(('0.0.0.0', 8088), app)
    server.serve_forever()
    # 这里指定了地址和端口号。


