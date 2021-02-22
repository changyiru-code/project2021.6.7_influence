# # 模型第三步，读取mongodb数据库，只读取一个事件，运行公式模型，计算单独一个事件的影响力，输出结果格式为字典，进行归一化
# 读取数据库里的测试数据，验证模型
# 整理代码，使代码逻辑清晰

# 导包
from pymongo import MongoClient
import pandas as pd
import numpy as np
from datetime import datetime
import json

# 创建连接MongoDB数据库函数
def connection():
    # 1:账号密码方式连接本地MongoDB数据库服务 | "mongodb://用户名:密码@公网ip:端口/"
    conn = MongoClient("mongodb://root:19980529@127.0.0.1:27017/")  # 用户名、密码可修改
    # 2:连接本地数据库(influence)和集合
    collection = conn["influence"]["keyword1_status"]
    data = collection.find()
    data = list(data)  # 在转换成列表时，可以根据情况只过滤出需要的数据。(for遍历过滤)
    return data


# 计算时间差的函数
def timecha(time1, time2):
    diff_day = (time1 - time2).days
    diff_sec = (time1 - time2).seconds
    m, s = divmod(diff_sec, 60)
    h, m = divmod(m, 60)
    if (diff_day == 0 and (h != 0 or m != 0 or s != 0)) or h > 12:
        T = diff_day + 1   # 如果时间差超过12小时，则按一天算，不足12时不按一天算
        print(T)  # 时间单元数差
    else:
        T = diff_day
        print("时间差", T)  # 时间单元数差
    return T


# 读取事件集合，获得转发，评论数；微博文章数；持续时间；时间单元数差；爬虫起止时间
def read_event(data):

    # li_count = []  # 存放每个话题里的微博文章数Mj
    # li_T = []  # 话题持续时间Tj
    # li_dt = []  # 当前时间与话题首次发布时间的时间单元数差det(tj)
    # li_starttime = []   # 每个事件的开始时间
    # li_endtime = []   # 每个事件的结束时间

    # 1读取数据
    # df1 = pd.DataFrame(data, columns=['repostsCount', 'commentsCount'])    # 这句可以不要
    df1 = pd.DataFrame(data)    # 读取集合的全部数据
    df2 = df1[['repostsCount', 'commentsCount']]  # 只提取转发和评论
    # df2 = df2.apply(pd.to_numeric)  # 如果转发和评论是object类型求和结果为inf,则去掉该句注释，转化数据类型为数值型
    print(df2)
    ylist_sum = df2.sum(axis=0)
    print(ylist_sum)
    li_all = ylist_sum.values.tolist()  # 将dataframe类型的值转换成列表
    print(li_all)  # li_all存放每个话题的全部转发，评论数

    # 2求事件的文章个数Mj
    li_count = df1.index.size  # 行数
    print(li_count)

    # 3求每个话题的持续时间Tj
    mod_times = df1['createAt']  # 提取每一行的时间
    print(mod_times.tolist())
    mod_times = [datetime.strptime(x, r"%Y-%m-%d %H:%M:%S") for x in mod_times]
    print(mod_times)
    max_time = max(mod_times)  # 该话题的结束时间
    min_time = min(mod_times)  # 该话题的开始时间
    li_T = timecha(max_time, min_time)   # 该话题的持续时间
    print(li_T)

    # # 4定义爬虫的起止时间   要修改公式这里
    # li_starttime.append(min_time)
    # li_endtime.append(max_time)

    # 5获取当地时间,格式化成2016-03-20 11:45:39形式,获得当前时间与话题首次发布时间的时间单元数差
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当地时间
    now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')  # 改str类型为datetime.datetime类型
    li_dt = timecha(now, min_time)
    print(li_dt)

    # # 计算爬虫的起止时间
    # end_time = max(li_endtime)  # 每个事件结束时间的最大值，得到爬虫的结束时间
    # start_time = min(li_starttime)  # 每个事件开始时间的最小值，得到爬虫的开始时间
    # n_dt = timecha(end_time, start_time)   # 爬虫的起止时间
    # print(n_dt)  # 爬虫的起止时间

    print("====")
    print(li_all)  # [[1, 2290, 2280, 2155], [2, 3060, 2898, 2782], [3, 2021, 2041, 1855]]
    print(li_count)  # [24, 32, 21]
    print(li_T)  # [448, 448, 464]
    print(li_dt)
    # print(n_dt)  # 爬虫的起止时间
    return li_all, li_count, li_T, li_dt
    # return li_all, li_count, li_T, li_dt, n_dt


# 创建主函数
def main():
    # 连接数据库，得到集合数据
    data = connection()
    # # 数据集的基本路径,可根据情况修改
    # path_base = 'D:\my_file\研究生期间的资料\影响力评价模型-参考论文\司法案件影响力评估-项目\data-all\data-all\status\status-by-keyword'
    #
    # 1、读取集合中的事件数据，计算该事件的总转发，总评论，存入huati1.csv文件
    # li_all, li_count, li_T, li_dt, n_dt = read_event(data)
    li_all, li_count, li_T, li_dt = read_event(data)
    print(li_all)  # 事件的全部转发和评论数
    print(li_count)  # [24, 32, 21]每个话题里的微博文章数Mj
    print(li_T)  # [448, 448, 464]话题持续时间Tj
    print(li_dt)   # 当前时间与话题首次发布时间的时间单元数差det(tj)
    # print(n_dt)  # 爬虫的起止时间
    #
    # 计算公式中的除法
    count_result = np.log(li_count)
    print(count_result)  # exp(Mj/M)改成ln(Mj)  计算话题覆盖度
    topic_coverage = np.arctan(count_result)*2/np.pi*100
    print(topic_coverage)

    #
    #
    li_count_result = np.log(li_count / li_T)
    print(li_count_result)  # ln(Mj/Tj) 计算话题活跃度
    topic_activity = np.arctan(li_count_result)*2/np.pi*100
    print(topic_activity)

    #
    #
    li_dt_result = 1 / (np.power(li_dt, 0.1))
    print(li_dt_result)  # (dt+1)^-0.1 计算话题新颖度
    topic_novelty = np.arctan(li_dt_result)*2/np.pi*100
    print(topic_novelty)

    #
    #
    n_result = np.log(li_T)
    print(n_result)  # nu/n改成ln(nu)  计算话题持久度
    topic_persistence = np.arctan(n_result)*2/np.pi*100
    print(topic_persistence)

    #
    #
    score = np.log(sum(li_all))
    print(score)  #   计算用户参与度
    user_engage = np.arctan(score)*2/np.pi*100
    print(user_engage)
    #
    dict1 = {}   # 存放最后的结果，字典形式
    list1 = []    # 存放每个话题各评价指标及总影响力值，列表形式

    influence = score * li_count_result * count_result * n_result * li_dt_result
    print(influence)     # 总公式  话题影响力值
    b = len(str(int(influence)))

    topic_influence = np.arctan(influence/np.power(10, b - 1))*2/np.pi*100
    print(topic_influence)  #总影响力值除以其  整数位数-1，再反正切归一化，再乘以100

    #
    # 将每个话题的对应结果存入列表
    dict2 = {}
    dict2["topic_influence"] = topic_influence
    dict2["user_engage"] = user_engage
    dict2["topic_coverage"] = topic_coverage
    dict2["topic_activity"] = topic_activity
    dict2["topic_novelty"] = topic_novelty
    dict2["topic_persistence"] = topic_persistence
    list1.append(dict2)
    print(list1)  # 字典格式
    #
    dict1["result"] = list1
    print(dict1)  # 字典格式
    result = json.dumps(dict1)  # 将字典转化为json字符串
    print(result)    # json格式
    # d1 = json.loads(j)  # 将json字符串转化为字典


main()
