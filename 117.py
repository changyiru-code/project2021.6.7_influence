# # 模型第三步，读取mongodb数据库，遍历读取集合下面的全部话题,运行公式模型，同时计算多个话题影响力，修改输出结果格式为字典，进行归一化
#与116的区别是116时间以天为单位，117时间以时为单位
# 读取测试数据，验证模型
# 整理代码，使代码逻辑清晰
import os
import copy
import csv
from pymongo import MongoClient
import pandas as pd
import numpy as np
from datetime import datetime
import json
import re


# 创建连接MongoDB数据库函数
def connection():
    # 1:账号密码方式连接本地MongoDB数据库服务 | "mongodb://用户名:密码@公网ip:端口/"
    conn = MongoClient("mongodb://root:19980529@127.0.0.1:27017/")  # 用户名、密码可修改
    # 2:连接本地数据库(influence)和集合
    db = conn["influence"]

    col_names = db.list_collection_names(session=None)  # pymongo获取指定数据库的集合名称
    # print(col_names)

    data_list = []
    tid_list = []
    for title in col_names:
        # print(title)
        # 获取集合里的数据
        collection = db[title]
        data = collection.find()
        data = list(data)  # 在转换成列表时，可以根据情况只过滤出需要的数据。(for遍历过滤)
        # print(data)
        data_list.append(data)

        # 获取集合里的话题id
        num = re.compile(r'\d')
        tid = num.search(title).group()
        # print(tid)
        tid_list.append(tid)
    tid_list = [int(x) for x in tid_list]
    return data_list, tid_list



# 计算时间差的函数
def timecha(time1, time2):
    diff_day = (time1 - time2).days
    diff_sec = (time1 - time2).seconds
    m, s = divmod(diff_sec, 60)  # 时间差是diff_day天h时m分s秒
    h, m = divmod(m, 60)
    h_cha = diff_day * 24 + h   # 时间差，以时为单位
    print(h_cha)
    if (h == 0 and (m != 0 or s != 0)) or m > 30:
        T = h_cha + 1   # 如果时间差超过12小时，则按一天算，不足12时不按一天算
        print(T)  # 时间单元数差
    else:
        T = h_cha
        print("时间差", T)  # 时间单元数差
    return T


# 读取数据库，获得转发，评论数；微博文章数；持续时间；时间单元数差；爬虫起止时间
def read_event(data_list):
    li_all = []  # 存放每个话题的全部转发，评论数
    li_count = []  # 存放每个话题里的微博文章数Mj
    li_T = []  # 话题持续时间Tj
    li_dt = []  # 当前时间与话题首次发布时间的时间单元数差det(tj)
    li_starttime = []   # 每个事件的开始时间
    li_endtime = []   # 每个事件的结束时间
    for data in data_list:
        # 1读取数据
        df1 = pd.DataFrame(data)  # 读取集合的全部数据
        df2 = df1[['repostsCount', 'commentsCount']]  # 只提取转发和评论
        # df2 = df2.apply(pd.to_numeric)  # 如果转发和评论是object类型求和结果为inf,则去掉该句注释，转化数据类型为数值型
        # print(df2)
        ylist_sum = df2.sum(axis=0)
        # print(ylist_sum)
        li_ylist_sum = ylist_sum.values.tolist()  # 将dataframe类型的值转换成列表
        li = []
        li.extend(li_ylist_sum)
        li_all.append(li)
        print(li_all)  # li_all存放每个话题的全部转发，评论数

        # 2求每个话题的文章个数Mj
        rows = df1.index.size  # 行数
        li_count.append(rows)
        print(li_count)  # li_all存放每个话题的全部转发，评论数


        # 3求每个话题的持续时间Tj
        mod_times = df1['createAt']  # 提取每一行的时间
        print(mod_times.tolist())
        mod_times = [datetime.strptime(x, r"%Y-%m-%d %H:%M:%S") for x in mod_times]
        max_time = max(mod_times)  # 该话题的结束时间
        min_time = min(mod_times)  # 该话题的开始时间
        T = timecha(max_time, min_time)   # 该话题的持续时间
        li_T.append(T)
        print(li_T)


        # 4定义爬虫的起止时间
        li_starttime.append(min_time)
        li_endtime.append(max_time)

        # 5获取当地时间,格式化成2016-03-20 11:45:39形式,获得当前时间与话题首次发布时间的时间单元数差
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当地时间
        now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')  # 改str类型为datetime.datetime类型
        dt = timecha(now, min_time)
        li_dt.append(dt)
        print(li_dt)


    # 计算爬虫的起止时间
    end_time = max(li_endtime)  # 每个事件结束时间的最大值，得到爬虫的结束时间
    start_time = min(li_starttime)  # 每个事件开始时间的最小值，得到爬虫的开始时间
    n_dt = timecha(end_time, start_time)   # 爬虫的起止时间

    print(n_dt)  # 爬虫的起止时间
    print(li_all)  # [[1, 2290, 2280, 2155], [2, 3060, 2898, 2782], [3, 2021, 2041, 1855]]
    print(li_count)  # [24, 32, 21]
    print(li_T)  # [448, 448, 464]
    M = sum(li_count)
    print(M)  # 所有话题的全部文章数
    print(li_dt)
    #
    return li_all, li_count, li_T, M, li_dt, n_dt


# 定义熵值法函数
def cal_weight(x):
    '''熵值法计算变量的权重'''
    fenshu = copy.deepcopy(x)
    # 标准化
    fenshu = fenshu.apply(lambda fenshu: ((fenshu - np.min(fenshu)) / (np.max(fenshu) - np.min(fenshu))))
    print(fenshu)
    # 求k
    rows = fenshu.index.size  # 行
    print(rows)
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
    print('w:', w)
    add_wi = x * w
    print(add_wi)
    score = add_wi.sum(axis=1)
    print(score)
    score = score.tolist()
    print(score)
    return score


# 将各评价指标结果归一化
def normalize(count_result):
    func = lambda x: np.exp(x)
    result = map(func, count_result)
    exp_count_result = list(result)
    print(exp_count_result)  # exp()  先对结果求指数

    func = lambda x: np.log(x)/np.log(max(exp_count_result))
    result = map(func, exp_count_result)
    norm_result = list(result)
    print(norm_result)  # ln(x)/ln(max) 话题各指标归一化，范围[0,1]

    norm_result = [i * 100 for i in norm_result]
    return norm_result    # 乘以100，得到范围[0,100]


def main():
    # 连接数据库，得到集合数据
    data_list, tid_list = connection()
    # print(data_list)    #
    # print('topic id: ', tid_list)

    # 1、读取数据集的基本路径下的每一个话题csv文件，计算每个话题的总转发，总评论，存入huati1.csv文件
    li_all, li_count, li_T, M, li_dt, n_dt = read_event(data_list)    #
    print(li_all)  # 事件的全部转发和评论数
    print(li_count)  # [24, 32, 21]每个话题里的微博文章数Mj
    print(li_T)  # [448, 448, 464]话题持续时间Tj
    print(M)  # 所有话题的全部文章数
    print(li_dt)   # 当前时间与话题首次发布时间的时间单元数差det(tj)
    print(n_dt)  # 爬虫的起止时间

    # 计算公式中的除法
    func = lambda x: np.exp(x / M)
    result = map(func, li_count)
    count_result = list(result)
    print(count_result)  # exp(Mj/M)  计算话题覆盖度

    norm_cover_result=normalize(count_result)  #归一化覆盖度值
    print(norm_cover_result)

    func1 = lambda x, y: np.log(x / y)
    result = map(func1, li_count, li_T)
    li_count_result = list(result)
    print(li_count_result)  # ln(Mj/Tj) 计算话题活跃度

    norm_activity_result=normalize(li_count_result)  # 归一化活跃度值
    print(norm_activity_result)

    func2 = lambda x: 1 / (np.power(x, 0.1)) # 也可以将0.1改成0.5，参考论文是0.5
    result = map(func2, li_dt)
    li_dt_result = list(result)
    print(li_dt_result)  # (dt+1)^-0.1 计算话题新颖度

    norm_novelty_result = normalize(li_dt_result)  # 归一化新颖度值
    print(norm_novelty_result)

    func3 = lambda x: x / n_dt
    result = map(func3, li_T)
    n_result = list(result)
    print(n_result)  # nu/n  计算话题持久度

    norm_persist_result=normalize(n_result)  # 归一化持久度值
    print(norm_persist_result)

    # #  2、读取li_all的转发数和评论数，利用熵权法计算每个话题转发，评论对话题影响力的贡献值
    # # 1读取数据
    repose_comment = pd.DataFrame(li_all, columns=['该话题总转发数', '该话题总评论数'])
    print(repose_comment)
    # 2数据预处理 ,去除空值的记录
    repose_comment.dropna()
    score = cal_weight(repose_comment)
    print(score)

    #用户参与度归一化
    func4 = lambda x: np.log(x)/np.log(max(score))
    result = map(func4, score)
    norm_score_result = list(result)  # ln(x)/ln(max) 话题影响力归一化

    user_engage = [i * 100 for i in norm_score_result]
    print(user_engage)  # l话题影响力归一化,乘以100

    m = 1   # 话题id
    dict1 = {}   # 存放最后的结果，字典形式
    list1 = []    # 存放每个话题各评价指标及总影响力值，列表形式

    influence = [score[i] * li_count_result[i] * count_result[i] * n_result[i] * li_dt_result[i] for i in range(len(score))]
    print(influence)     # 总公式  话题影响力值

    # 话题影响力总值归一化
    func4 = lambda x: np.log(x)/np.log(max(influence))
    result = map(func4, influence)
    norm_influ_result = list(result)  # ln(x)/ln(max) 话题影响力归一化

    norm_influ_result = [i * 100 for i in norm_influ_result]
    print(norm_influ_result)  # l话题影响力归一化,乘以100

    # 将每个话题的对应结果存入列表
    for i in range(len(norm_influ_result)):
        dict2 = {}
        dict2["topic"] = tid_list[i]
        dict2["topic_influence"] = norm_influ_result[i]
        dict2["user_engage"] = user_engage[i]
        dict2["topic_coverage"] = norm_cover_result[i]
        dict2["topic_activity"] = norm_activity_result[i]
        dict2["topic_novelty"] = norm_novelty_result[i]
        dict2["topic_persistence"] = norm_persist_result[i]
        m = m+1
        list1.append(dict2)
    print(list1)  # 字典格式

    list1 = sorted(list1, key=lambda list1: list1["topic_influence"], reverse=True)
    print("降序后列表:{}".format(list1))
    dict1["result"] = list1
    print(dict1)  # 字典格式
    result = json.dumps(dict1)  # 将字典转化为json字符串
    print(result)    # json格式
    # d1 = json.loads(j)  # 将json字符串转化为字典

main()
