# # 模型第三步，读取mongodb数据库，只读取一个事件，时间以时为单位，运行公式模型，计算单独一个事件的影响力，输出结果格式为字典，进行归一化
# 读取数据库里的测试数据，验证模型
# 存入数据库

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
    collection = conn["influence"]["keyword6_status"]
    data = collection.find()
    data = list(data)  # 在转换成列表时，可以根据情况只过滤出需要的数据。(for遍历过滤)
    return data


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


# 读取事件集合，获得转发，评论数；微博文章数；持续时间；时间单元数差；爬虫起止时间
def event_influ_calcu(data):
    # 1:读取数据集的事件数据，计算事件的所需内容
    # 1读取数据
    df1 = pd.DataFrame(data)    # 读取集合的全部数据
    df2 = df1[['repostsCount', 'commentsCount']]  # 只提取转发和评论
    ylist_sum = df2.sum(axis=0)
    li_all = ylist_sum.values.tolist()  # 将dataframe类型的值转换成列表

    # 2求事件的文章个数Mj
    li_count = df1.index.size  # 行数

    # 3求每个话题的持续时间Tj
    mod_times = df1['createAt']  # 提取每一行的时间
    mod_times = [datetime.strptime(x, r"%Y-%m-%d %H:%M:%S") for x in mod_times]
    max_time = max(mod_times)  # 该话题的结束时间
    min_time = min(mod_times)  # 该话题的开始时间
    li_T = timecha(max_time, min_time)   # 该话题的持续时间

    # 4获取当地时间,格式化成2016-03-20 11:45:39形式,获得当前时间与话题首次发布时间的时间单元数差
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当地时间
    now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')  # 改str类型为datetime.datetime类型
    li_dt = timecha(now, min_time)

    # 2:计算公式中的各个指标
    count_result = np.log(li_count)  # exp(Mj/M)改成ln(Mj)  计算话题覆盖度
    topic_coverage = np.arctan(count_result)*2/np.pi*100  # 归一化覆盖度值

    li_count_result = np.log(li_count / li_T)  # ln(Mj/Tj) 计算话题活跃度
    topic_activity = np.arctan(li_count_result)*2/np.pi*100  # 归一化活跃度值

    li_dt_result = 1 / (np.power(li_dt, 0.1))  # (dt+1)^-0.1 计算话题新颖度
    topic_novelty = np.arctan(li_dt_result)*2/np.pi*100  # 归一化新颖度值

    n_result = np.log(li_T)  # nu/n改成ln(nu)  计算话题持久度
    topic_persistence = np.arctan(n_result)*2/np.pi*100  # 归一化持久度值

    score = np.log(sum(li_all))  #   计算用户参与度
    user_engage = np.arctan(score)*2/np.pi*100   # 用户参与度归一化

    # 3:计算总公式  话题影响力值
    dict1 = {}   # 存放最后的结果，字典形式
    list1 = []    # 存放每个话题各评价指标及总影响力值，列表形式
    influence = score * li_count_result * count_result * n_result * li_dt_result     # 总公式  话题影响力值
    b = len(str(int(influence)))
    topic_influence = np.arctan(influence/np.power(10, b - 1))*2/np.pi*100  #总影响力值除以其  整数位数-1，再反正切归一化，再乘以100

    # 4:将每个话题的对应结果存入列表
    dict2 = {}
    dict2["topic_influence"] = topic_influence
    dict2["user_engage"] = user_engage
    dict2["topic_coverage"] = topic_coverage
    dict2["topic_activity"] = topic_activity
    dict2["topic_novelty"] = topic_novelty
    dict2["topic_persistence"] = topic_persistence
    list1.append(dict2)
    dict1["result"] = list1
    return dict1


def save_to_db(dict1):
    # 1:账号密码方式连接本地MongoDB数据库服务 | "mongodb://用户名:密码@公网ip:端口/"
    conn = MongoClient("mongodb://root:19980529@127.0.0.1:27017/")  # 用户名、密码可修改
    # 2:连接本地分析结果数据库(influence)和集合(event_influence)
    db = conn["influence_result"]['event_influence']
    db.delete_many({})
    db.insert_one(dict1)


# 创建主函数
def main():
    # 1：消息服务接口,接收数据导入成功的通知，没写

    # 2：连接数据库，得到集合数据，数据库访问接口，要改接口
    # 收到通知后，以事件id作为参数调用提供的一个事件关联数据查询接口翻页查询事件关联的数据进行事件影响力分析。
    # 怎么通过id访问，目前是通过数据库名和集合名读取数据
    data = connection()

    # 3：影响力计算
    dict1 = event_influ_calcu(data)

    # 4：将计算结果存入数据库
    save_to_db(dict1)

    # 5：消息服务接口,通知计算完成，给出存数据的数据库名和集合名，没写


main()
