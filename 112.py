##模型第三步，读取csv文件，运行公式模型，修改输出结果格式为字典，进行归一化
import os
import pandas as pd
import copy
import csv
import numpy as np
from datetime import datetime
import time
import json
def timecha(time1,time2):
    diff_day = (time1 - time2).days
    diff_sec = (time1 - time2).seconds
    m, s = divmod(diff_sec, 60)
    h, m = divmod(m, 60)
    # print("%d days,%02d hours,%02d minites,%02d seconds" % (diff_day, h, m, s))
    if (diff_day == 0 and (h != 0 or m != 0 or s != 0)) or h > 12:
        T = diff_day + 1
        print(T)  # 当前时间与话题首次发布时间的时间单元数差
    else:
        T = diff_day
        print("时间差",T)  # 当前时间与话题首次发布时间的时间单元数差
    return T
def read_each_huati(path_base):
    p = os.walk(path_base)  # html文件夹路径
    li_all = []  # 存放每个话题的全部点赞，转发，评论数
    li_count = []  # 存放每个话题里的微博文章数Mj
    li_T = []  # 话题持续时间T
    li_dt = []  # 当前时间与话题首次发布时间的时间单元数差+1
    count = 1
    for path, dir_list, file_list in p:
        for file_name in file_list:
            # print(file_name)
            path = os.path.join(path_base, file_name)
            # print(path)
            path = path.replace("\\", "\\\\")
            # print(path)
            # 1读取数据
            df1 = pd.read_csv(path, usecols=['zan','zhuanfa', 'pinglun'],encoding='utf-8')
            # print(df1)
            ylist_sum = df1.sum(axis=0)
            li_ylist_sum=ylist_sum.values.tolist()
            # print(li_ylist_sum)  #将dataframe类型的值转换成列表
            li = []
            li.append(count)
            li.extend(li_ylist_sum)
            # print(li)
            li_all.append(li)
            count = count + 1
            # 求每个话题的文章个数Mj
            rows = df1.index.size  # 行
            # print(rows)
            li_count.append(rows)
            with open(path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                # print(reader)
                mod_times = [row[7] for row in reader]  #提取每一行的时间
            mod_times = [time.strptime(x, u"%m月%d日") for x in mod_times[1:]]
            mod_times = [time.strftime("%m/%d", x) for x in mod_times]#将月日改成 /
            mod_times = [datetime.strptime(x, r"%m/%d") for x in mod_times]#将字符串类型转成时间类型
            max_time = max(mod_times)
            min_time = min(mod_times)
            # print(type(max_time))
            T=timecha(max_time,min_time)
            li_T.append(T)
            # 获取当地时间,格式化成2016-03-20 11:45:39形式
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当地时间
            now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')  # 改str类型为datetime.datetime类型
            dt=timecha(now,min_time)
            li_dt.append(dt)

        print(li_all)  # [[1, 2290, 2280, 2155], [2, 3060, 2898, 2782], [3, 2021, 2041, 1855]]
        print(li_count)  # [24, 32, 21]
        print(li_T)  # [448, 448, 464]
        M = sum(li_count)
        print(M)  # 所有话题的全部文章数
        print(li_dt)

    # huaticsv_path = os.path.join(path_base, 'huati.csv').replace("\\", "\\\\")
    # with open(huaticsv_path, "a", encoding='utf-8', newline='') as csvfile:  # 写csv文件表头
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['话题', '该话题总赞数', '该话题总转发数', '该话题总评论数'])
    #     for li in li_all:
    #         writer.writerow(li)
    return li_count, li_T, M, li_dt


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
    print(type(score))
    score = score.tolist()
    print(score)
    print(type(score))
    return score
def normalize(count_result):
    func = lambda x: np.exp(x)
    result = map(func, count_result)
    exp_count_result = list(result)
    print(exp_count_result)  # exp(Mj/M)  话题覆盖度

    func = lambda x: np.log(x)/np.log(max(exp_count_result))
    result = map(func, exp_count_result)
    norm_result = list(result)
    print(norm_result)  # ln(x)/ln(max) 话题影响力归一化

    norm_result = [i * 100 for i in norm_result]
    return norm_result

def main():
    path_base = 'data'

    # 1、读取每一个话题csv文件，计算每个话题的总赞，总转发，总评论，存入huati.csv文件
    li_count, li_T, M, li_dt = read_each_huati(path_base)

    print(li_count)  # [24, 32, 21]Mj
    print(li_T)  # [448, 448, 464]T
    print(M)  # 所有话题的全部文章数
    print(li_dt)

    # 定义爬虫的起止时间
    start_time = '2020-04-01 00:00:00'
    end_time = '2020-04-30 23:59:59'
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')  # 改str类型为datetime.datetime类型
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')  # 改str类型为datetime.datetime类型
    n_dt=timecha(end_time, start_time)
    print(n_dt)  # 爬虫的起止时间

 #计算公式中的除法

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

    norm_activity_result=normalize(li_count_result)  #归一化活跃度值
    print(norm_activity_result)

    func2 = lambda x: 1 / (np.power(x, 0.1)) #也可以将0.1改成0.5，参考论文是0.5
    result = map(func2, li_dt)
    li_dt_result = list(result)
    print(li_dt_result)  # (dt+1)^-0.1 计算话题新颖度

    norm_novelty_result=normalize(li_dt_result)  #归一化新颖度值
    print(norm_novelty_result)

    func3 = lambda x: x / n_dt
    result = map(func3, li_T)
    n_result = list(result)
    print(n_result)  # nu/n  计算话题持久度

    norm_persist_result=normalize(n_result)  #归一化持久度值
    print(norm_persist_result)

    #  2、读取huati.csv文件，利用熵权法计算每个话题赞，转发，评论对话题影响力的贡献值
    # 1读取数据
    df = pd.read_csv(('huati.csv').replace("\\", "\\\\"), encoding='utf-8')
    # df = pd.read_csv(os.path.join(path_base, 'huati.csv').replace("\\", "\\\\"), encoding='utf-8')
    # 2数据预处理 ,去除空值的记录
    df.dropna()
    # 去掉“话题”这个指标
    df.drop(columns="话题", axis=1, inplace=True)
    score = cal_weight(df)
    print(score)
 #    print(li_count_result)  # ln(Mj/Tj)
 #    print(count_result)  # exp(Mj/M)
 #    print(n_result)  # nu/n
 #    print(li_dt_result)  # (dt+1)^-0.1
    m=1
    dict1={}
    list1=[]

    influence=[score[i] * li_count_result[i] * count_result[i] * n_result[i] * li_dt_result[i] for i in range(len(score))]
    print(influence) #总公式  话题影响力值

    func4 = lambda x: np.log(x)/np.log(max(influence))
    result = map(func4, influence)
    norm_influ_result = list(result)
    # print(li_influ_result)  # ln(x)/ln(max) 话题影响力归一化

    norm_influ_result = [i * 100 for i in norm_influ_result]
    print(norm_influ_result)  # ln(x)/ln(max) 话题影响力归一化,乘以100

    for i in range(len(norm_influ_result)):
        dict2={}
        dict2["topic"]=m
        dict2["topic_influence"]=norm_influ_result[i]
        dict2["topic_coverage"] = norm_cover_result[i]
        dict2["topic_activity"] = norm_activity_result[i]
        dict2["topic_novelty"] = norm_novelty_result[i]
        dict2["topic_persistence"] = norm_persist_result[i]
        m=m+1
        list1.append(dict2)
    print(list1)  #字典格式

    dict=sorted(list1, key=lambda list1: list1["topic_influence"], reverse=True)
    print("降序后列表:{}".format(dict))
    dict1["result"] = dict
    print(dict1)  #字典格式
    result = json.dumps(dict1)  #将字典转化为json字符串
    print(result) #json格式
    # d1 = json.loads(j)  #将json字符串转化为字典


main()
