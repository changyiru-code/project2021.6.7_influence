#简化一下代码，将相同的部分封装成一个函数调用，再复制粘贴到公式后半部分.py
import os
import pandas as pd
import copy
import csv
import numpy as np
from datetime import datetime
def timecha(time1,time2):
    diff_day = (time1 - time2).days
    diff_sec = (time1 - time2).seconds
    m, s = divmod(diff_sec, 60)
    h, m = divmod(m, 60)
    print("%d days,%02d hours,%02d minites,%02d seconds" % (diff_day, h, m, s))
    if (diff_day == 0 and (h != 0 or m != 0 or s != 0)) or h > 12:
        T = diff_day + 1
        print(T)  # 当前时间与话题首次发布时间的时间单元数差
    else:
        T = diff_day
        print(T)  # 当前时间与话题首次发布时间的时间单元数差
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
            print(file_name)
            path = os.path.join(path_base, file_name)
            print(path)
            path = path.replace("\\", "\\\\")
            print(path)
            # 1读取数据
            df = pd.read_csv(path, encoding='utf-8')
            print(df)
            # 去掉“微博”这个指标
            df1 = copy.deepcopy(df)
            df1.drop(columns=["微博", "pub_time"], axis=1, inplace=True)
            print(df1)
            ylist_sum = df1.sum(axis=0)
            print(ylist_sum)
            print(type(ylist_sum))
            li = []
            li.append(count)
            for i in ylist_sum:
                print(i)
                li.append(i)
            li_all.append(li)
            count = count + 1
            # 求每个话题的文章个数Mj
            rows = df.index.size  # 行
            print(rows)
            li_count.append(rows)
            with open(path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                mod_times = [row[4] for row in reader]
            mod_times = [datetime.strptime(x, r"%Y/%m/%d %H:%M") for x in mod_times[1:]]
            max_time = max(mod_times)
            min_time = min(mod_times)

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
    huaticsv_path = os.path.join(path_base, 'huati.csv').replace("\\", "\\\\")
    with open(huaticsv_path, "a", encoding='utf-8', newline='') as csvfile:  # 写csv文件表头
        writer = csv.writer(csvfile)
        writer.writerow(['话题', '该话题总赞数', '该话题总转发数', '该话题总评论数'])
        for li in li_all:
            writer.writerow(li)
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


def main():
    path_base = 'D:\\常艺茹的文档\\研究生期间的资料\\影响力评价模型-参考论文\\influence_el'
    # 1、读取每一个话题csv文件，计算每个话题的总赞，总转发，总评论，存入huati.csv文件
    li_count, li_T, M, li_dt = read_each_huati(path_base)
    print(li_count)  # [24, 32, 21]Mj
    print(li_T)  # [448, 448, 464]T
    print(M)  # 所有话题的全部文章数
    print(li_dt)
    # 定义爬虫的起止时间，计算
    start_time = '2019-03-19 10:35:00'
    end_time = '2020-03-19 20:35:00'
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')  # 改str类型为datetime.datetime类型
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')  # 改str类型为datetime.datetime类型
    n_dt=timecha(end_time, start_time)
    print(n_dt)  # 爬虫的起止时间
 #计算公式中的除法
    func = lambda x, y: np.log(x / y)
    result = map(func, li_count, li_T)
    li_count_result = list(result)
    print(li_count_result)  # ln(Mj/Tj)
    func1 = lambda x: np.exp(x / M)
    result = map(func1, li_count)
    count_result = list(result)
    print(count_result)  # exp(Mj/M)
    func2 = lambda x: x / n_dt
    result = map(func2, li_T)
    n_result = list(result)
    print(n_result)  # nu/n
    func3 = lambda x: 1 / (np.power(x, 0.1)) #也可以将0.1改成0.5，参考论文是0.5
    result = map(func3, li_dt)
    li_dt_result = list(result)
    print(li_dt_result)  # (dt+1)^-0.1

    #  2、读取huati.csv文件，利用熵权法计算每个话题赞，转发，评论对话题影响力的贡献值
    # 1读取数据
    df = pd.read_csv(os.path.join(path_base, 'huati.csv').replace("\\", "\\\\"), encoding='utf-8')
    # 2数据预处理 ,去除空值的记录
    df.dropna()
    # 去掉“话题”这个指标
    df.drop(columns="话题", axis=1, inplace=True)
    score = cal_weight(df)
    print(score)
    print(li_count_result)  # ln(Mj/Tj)
    print(count_result)  # exp(Mj/M)
    print(n_result)  # nu/n
    print(li_dt_result)  # (dt+1)^-0.1
    for i in range(len(score)):
        ji = score[i] * li_count_result[i] * count_result[i] * n_result[i] * li_dt_result[i]
        print(ji)


main()

# -5762.334142537879
# -7889.981180289497
# -5329.685504112602