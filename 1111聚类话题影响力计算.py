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


def event_influ_calcu(cluster_text):
    # 1:读取数据集的每一个话题数据，计算每个话题的所需内容
    # 读取数据库，获得转发，评论数；微博文章数；持续时间；时间单元数差；爬虫起止时间
    li_all = []  # 存放每个话题的全部转发，评论数
    li_count = []  # 存放每个话题里的微博文章数Mj
    li_T = []  # 话题持续时间Tj
    li_dt = []  # 当前时间与话题首次发布时间的时间单元数差det(tj)
    li_starttime = []   # 每个事件的开始时间
    li_endtime = []   # 每个事件的结束时间
    data_list = []   # 列表，[[{},{},...], [{},{},...], [{},{},...]]
    for li_i in range(len(cluster_text)):
        data_list.append(cluster_text[li_i])
    print(data_list)
    for data in data_list:
        # 1读取数据
        df1 = pd.DataFrame(data)  # 读取集合的全部数据
        df2 = df1[['repostsCount', 'commentsCount']]  # 只提取转发和评论
        ylist_sum = df2.sum(axis=0)
        li_ylist_sum = ylist_sum.values.tolist()  # 将dataframe类型的值转换成列表
        li = []
        li.extend(li_ylist_sum)
        li_all.append(li)

        # 2求每个话题的文章个数Mj
        rows = df1.index.size  # 行数
        li_count.append(rows)

        # 3求每个话题的持续时间Tj
        mod_times = df1['createAt']  # 提取每一行的时间
        mod_times = [datetime.strptime(x, r"%Y-%m-%d %H:%M:%S") for x in mod_times]
        max_time = max(mod_times)  # 该话题的结束时间
        min_time = min(mod_times)  # 该话题的开始时间
        T = timecha(max_time, min_time)   # 该话题的持续时间
        if T==0:
            li_T.append(T+0.1)
        else:
            li_T.append(T)
        # 4定义爬虫的起止时间
        li_starttime.append(min_time)
        li_endtime.append(max_time)

        # 5获取当地时间,格式化成2016-03-20 11:45:39形式,获得当前时间与话题首次发布时间的时间单元数差
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当地时间
        now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')  # 改str类型为datetime.datetime类型
        dt = timecha(now, min_time)
        li_dt.append(dt)

    # 计算爬虫的起止时间
    end_time = max(li_endtime)  # 每个事件结束时间的最大值，得到爬虫的结束时间
    start_time = min(li_starttime)  # 每个事件开始时间的最小值，得到爬虫的开始时间
    n_dt = timecha(end_time, start_time)   # 爬虫的起止时间

    M = sum(li_count)

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

    # 3:计算总公式  话题影响力值
    dict1 = {}   # 存放最后的结果，字典形式
    list1 = []    # 存放每个话题各评价指标及总影响力值，列表形式
    func = lambda x: np.exp(x)
    result = map(func, li_count_result)
    li_count_result = list(result)
    # li_count_result = [e_result+1 for e_result in list(result)]  # exp()  先对结果求指数 先对结果求指数,但是求对数以后还可能处于0-1之间，所以下面取对数就变成了负值

    influence = [score[i] * li_count_result[i] * count_result[i] * n_result[i] * li_dt_result[i] for i in range(len(score))]
    print(influence)
    # 话题影响力总值归一化
    func5 = lambda x: np.log(x)/np.log(max(influence))
    result = map(func5, influence)
    norm_influ_result = list(result)  # ln(x)/ln(max) 话题影响力归一化
    norm_influ_result = [i * 100 for i in norm_influ_result]  # l话题影响力归一化,乘以100

    # 4:将每个话题的对应结果存入列表
    for i in range(len(norm_influ_result)):
        dict2 = {}
        dict2["topic"] = "topic_name"
        dict2["topic_influence"] = norm_influ_result[i]
        dict2["user_engage"] = user_engage[i]
        dict2["topic_coverage"] = norm_cover_result[i]
        dict2["topic_activity"] = norm_activity_result[i]
        dict2["topic_novelty"] = norm_novelty_result[i]
        dict2["topic_persistence"] = norm_persist_result[i]
        list1.append(dict2)    # list1是字典格式

    list1 = sorted(list1, key=lambda list1: list1["topic_influence"], reverse=True)
    print("降序后列表:{}".format(list1))
    dict1["result"] = list1    # list1是字典格式
    return dict1


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
    print(cluster_text)    # 最终聚类结果
    # 3：影响力计算
    dict1 = event_influ_calcu(cluster_text)    #
    print(dict1)
    # event_influ_calcu(cluster_text)    #
# 创建连接MongoDB数据库函数
def connection():
    # 1:账号密码方式连接本地MongoDB数据库服务 | "mongodb://用户名:密码@公网ip:端口/"
    conn = MongoClient("mongodb://root:19980529@127.0.0.1:27017/")  # 用户名、密码可修改
    # 2:连接本地数据库(influence)和集合
    collection = conn["influence"]["keyword6_status"]
    data = collection.find()
    data = list(data)  # 在转换成列表时，可以根据情况只过滤出需要的数据。(for遍历过滤)
    # 根据hashtag聚类
    extract_hashtag(data)


# 创建主函数
def main():
    # 1：消息服务接口,接收数据导入成功的通知，没写

    # 2：连接数据库，得到集合数据，数据库访问接口，要改接口
    # 收到通知后，以事件id作为参数调用提供的一个事件关联数据查询接口翻页查询事件关联的数据进行事件影响力分析。
    # 怎么通过id访问，目前是通过数据库名和集合名读取数据
    connection()


main()

