## 1
# from pymongo import MongoClient
# import pprint
# import datetime
#
# # 账号密码方式连接MongoDB | "mongodb://用户名:密码@公网ip:端口/"
# client = MongoClient("mongodb://root:19980529@127.0.0.1:27017/")  # 用户名、密码可修改
#
# # 指定数据库
# db = client.test   # test是数据库名称，可修改
#
# # 指定集合
# collection = db.students  # students是集合名称，可修改
# from bson.objectid import ObjectId
#
# print(collection.find_one({'_id':ObjectId('6032693764a8ded99573437a')}))
#
# # # 插入数据
# # student = {'id': '20190101', 'name': 'Tom3', 'age': 20, 'gender': 'female'}
# # ret = collection.insert_one(student)  # collection.insert_one()方法 插入文档
# # print('insert_id:', ret.inserted_id)  # 插入文档时，如果文档尚未包含“_id”键，则会自动添加“_id”。
#
# # # 插入数据
# # student = {'id': '20190101', 'name': 'Tom3', 'age': 20, 'gender': 'female', 'class': '2001'}
# # ret = collection.insert_one(student)  # collection.insert_one()方法 插入文档
# # print('insert_id:', ret.inserted_id)  # 插入文档时，如果文档尚未包含“_id”键，则会自动添加“_id”。
#
# # 批量插入数据
# new_posts = [{"_id": 1002,
#                "author": "Curry",
#                "text": "Another post!",
#                "tags": ["bulk", "insert"],
#                "date": datetime.datetime(2017, 11, 12, 11, 14)},
#               {"_id": 1003,"author": "Maxsu",
#                "title": "MongoDB is fun",
#                "text": "and pretty easy too!",
#                "date": datetime.datetime(2019, 11, 10, 10, 45)}]
# ret = collection.insert_many(new_posts)  # 使用insert_many()来执行批量插入操作，这将在列表中插入每个文档，只向服务器发送一个命令
# print('insert_id:', ret.inserted_ids)  # 插入文档时，如果文档尚未包含“_id”键，则会自动添加“_id”。
#
# # # 使用find_one()获取单个文档
# # pprint.pprint(collection.find_one())  # 返回集合的第一个文档内容
# #
# # # 使用find_one("key":"value")获取满足条件的一个文档
# # pprint.pprint(collection.find_one({"age": "20"}))  # 返回集合中满足条件的一个文档内容
#
#
# # # 更新数据
# # condition = {'name': 'Tom3'}
# # edit = {'age': 21}
# # ret = collection.update_one(condition, {'$set': edit})
# # print('update:', ret.matched_count, ret.modified_count)
# #
# # # 查询
# # info = collection.find_one(condition)
# # print('select:', info)
# #
# # # 计数
# # count = collection.count_documents({})
# # print('count:', count)
# #
# # # 删除数据
# # ret = collection.delete_one(condition)
# # print('delete:', ret.deleted_count)



##2
# # coding=utf-8
# from pymongo import MongoClient  # 需要pip安装
# import pandas as pd
#
# client = MongoClient('192.168.0.11', 27017)  # 默认localhost，27017
# collection = client["数据库名"]["集合名"]
# data = collection.find()
# data = list(data)  # 在转换成列表时，可以根据情况只过滤出需要的数据。(for遍历过滤)
#
# df = pd.DataFrame(data)  # 读取整张表 (DataFrame)
# print(df)
# # 删除mongodb中的_id字段
# del data['_id']
# # 选择需要显示的字段
# data = data[['aear','cate','subcate','name','maxmoney','minmoney','time']]
# print(data)
# '''
#                         _id  name  age
# 0  59ba7f9b421aa91b08a43faa  张三   18
# 1  59ba7f9b421aa91b08a43fab  李四   20
# '''


##3
# import pycurl, json
# github_url = 'https://api.github.com/user/repos'
# user_pwd = "changyiru-code:529521zj..."
# data = json.dumps({
# 	"name": "test_repo",
# 	"description": "Some test repo"
# })
# c = pycurl.Curl()
# c.setopt(pycurl.URL, github_url)
# c.setopt(pycurl.USERPWD, user_pwd)
# c.setopt(pycurl.POST, 1)
# c.setopt(pycurl.POSTFIELDS, data)
# c.perform()

##4
# import threading
#
# def do_job():
#     print('Just do it!')
#     global timer
#     timer = threading.Timer(5, do_job)
#     timer.start()
#
# timer = threading.Timer(10, do_job)
# timer.start()


##5
# #上传json的post请求 r = requests.post(url,data=json,dumps(data))低版本
# #r = requests.post(url,json=data)高版本
# import requests
# import json
# url = "https://httpbin.org/post"
#
# headers = {'Content-Type': 'application/json;charset=UTF-8'}
#
# # data = {"info":{"code":1,"sex":"男","id":1900,"name":"巧吧软件测试"},
# #         "code":1,
# #         "name":"巧吧软件测试","sex":"女",
# #         "data":[{"code":1,"sex":"男","id":1900,"name":"巧吧软件测试"},{"code":1,"sex":"男","id":1900,"name":"巧吧软件测试"}],
# #         "id":1900}
# # data = {'eventNoticeType': 111, 'eventState': 222}
#
# # r = requests.post(url,data=json.dumps(data), headers=headers)
# # print(r.text.encode('utf-8').decode('unicode_escape'))  # .encode('utf-8').decode('unicode_escape')是输出中文
# # print(r.json()["data"].encode('utf-8').decode('unicode_escape'))
#
# # r = requests.post(url)
# # print(r.json().get("headers"))  # 这条语句与print(r.json()["headers"])等效


# ##6
# import requests
# import json
#
# url = 'https://api.github.com/events/notice'
# headers = {'Content-Type': 'application/json;charset=UTF-8'}
# meg = requests.post(url, headers=headers)
# # eventNoticeType = meg.json().get("eventNoticeType")
# # eventState = meg.json().get("eventState")
# # topicId = meg.json().get("topicId")
#
# # print(json.loads(r.text))   #r.json()与json.loads(r.text)等效
# print(meg.json())  #这两个print语句等效

##7
# import requests
# import json
# url = 'http://127.0.0.1:8888/accept'
# data = {'eventNoticeType': 111, 'eventState': 222}
#
# r = requests.post(url, data=json.dumps(data))
# print(r.json())  #这两个print语句等效


# ##8以下代码可以实现 一个HTTP接口供别人调用并post数据，但没法接收post回来的数据
# from flask import Flask, request, jsonify
# import json
# import requests
# import threading
#
# app = Flask(__name__)
# app.debug = True
#
#
# @app.route('/get/data/', methods=['post'])
# def add_stu():
#     if not request.data:  # 检测是否有数据
#         return ('fail')
#     student = request.data.decode('utf-8')
#     # 获取到POST过来的数据，因为我这里传过来的数据需要转换一下编码。根据晶具体情况而定
#     student_json = json.loads(student)
#     # 把区获取到的数据转为JSON格式。
#     print(student_json)
#
#     return jsonify(student_json)
#     # 返回JSON数据。
#
#
# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=1234)
#     # 这里指定了地址和端口号。


# # 9\coding:utf-8
#
# import json
# from wsgiref.simple_server import make_server
# import urllib.parse
# import re
#
#
# # 定义函数，参数是函数的两个参数，都是python本身定义的，默认就行了。
# def application(environ, start_response):
#     # 定义文件请求的类型和当前请求成功的code
#     start_response('200 OK', [('Content-Type', 'application/json')])
#     # environ是当前请求的所有数据，包括Header和URL，body
#
#     request_body = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0)))
#
#     json_str = request_body.decode('utf-8')  # byte 转 str
#     json_str = re.sub('\'', '\"', json_str)  # 单引号转双引号, json.loads 必须使用双引号
#     json_dict = json.loads(json_str)  # （注意：key值必须双引号）
#     print(json_dict["name"])
#
#     return [json.dumps(json_dict)]
#
#
# if __name__ == "__main__":
#     port = 6088
#     httpd = make_server("0.0.0.0", port, application)
#     print("serving http on port {0}...".format(str(port)))
#     httpd.serve_forever()


from pymongo import MongoClient
import pandas as pd
import numpy as np
from datetime import datetime
import json
import requests
import logging
import threading
import time

from flask import Flask, request, jsonify
import time
import requests
import sys
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.debug = True
from gevent import pywsgi


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
def event_influence_calculate(data):
    # 1:读取数据集的事件数据，计算事件的所需内容
    # 1读取数据
    logging.info("读取数据")  # jia1

    df1 = pd.DataFrame(data)    # 读取集合的全部数据
    df2 = df1[['repostsCount', 'commentsCount']]  # 只提取转发和评论
    ylist_sum = df2.sum(axis=0)
    li_all = ylist_sum.values.tolist()  # 将dataframe类型的值转换成列表

    logging.info("求事件的文章个数Mj")  # jia1

    # 2求事件的文章个数Mj
    li_count = df1.index.size  # 行数

    logging.info("求每个话题的持续时间Tj")  # jia1

    # 3求每个话题的持续时间Tj
    mod_times = df1['createdAt']  # 提取每一行的时间
    # print(mod_times.tolist())
    mod_times=[time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(x/1000)) for x in mod_times]
    mod_times = [datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in mod_times]  # 改str类型为datetime.datetime类型
    # print(mod_times)
    max_time = max(mod_times)  # 该话题的结束时间
    min_time = min(mod_times)  # 该话题的开始时间
    li_t = timecha(max_time, min_time)   # 该话题的持续时间

    logging.info("获取当地时间")  # jia1

    # 4获取当地时间,格式化成2016-03-20 11:45:39形式,获得当前时间与话题首次发布时间的时间单元数差
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当地时间
    now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')  # 改str类型为datetime.datetime类型
    li_dt = timecha(now, min_time)

    logging.info("计算公式中的各个指标")  # jia1

    # 2:计算公式中的各个指标
    count_result = np.log(li_count)  # exp(Mj/M)改成ln(Mj)  计算话题覆盖度
    topic_coverage = np.arctan(count_result)*2/np.pi*100  # 归一化覆盖度值

    li_count_result = np.exp(np.log(li_count / li_t))+0.5  # ln(Mj/Tj) 计算话题活跃度
    print("li_count_result:", li_count_result)
    topic_activity = np.arctan(li_count_result)*2/np.pi*100  # 归一化活跃度值

    li_dt_result = 1 / (np.power(li_dt, 0.1))  # (dt+1)^-0.1 计算话题新颖度
    topic_novelty = np.arctan(li_dt_result)*2/np.pi*100  # 归一化新颖度值

    n_result = np.log(li_t+1)  # nu/n改成ln(nu)  计算话题持久度
    topic_persistence = np.arctan(n_result)*2/np.pi*100  # 归一化持久度值

    score = np.log(sum(li_all))  #   计算用户参与度
    user_engage = np.arctan(score)*2/np.pi*100   # 用户参与度归一化

    logging.info("计算总公式")  # jia1

    # 3:计算总公式  话题影响力值
    dict1 = {}   # 存放最后的结果，字典形式
    list1 = []    # 存放每个话题各评价指标及总影响力值，列表形式
    influence = score * li_count_result * count_result * n_result * li_dt_result     # 总公式  话题影响力值
    b = len(str(int(influence)))
    topic_influence = np.arctan(influence/np.power(10, b - 1))*2/np.pi*100  #总影响力值除以其  整数位数-1，再反正切归一化，再乘以100

    logging.info("将每个话题的对应结果存入列表")  # jia1

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
    logging.info("连接数据库...")  # jia
    try:   # jia
        # 1:账号密码方式连接本地MongoDB数据库服务 | "mongodb://用户名:密码@公网ip:端口/"
        conn = MongoClient("mongodb://SOCIAL_ATTENTION:EF_KD_BJD-!24@10.20.2.181:28018/")  # 用户名、密码可修改
        # 2:连接本地分析结果数据库(SOCIAL_ATTENTION)和集合(social_influence)
        db = conn["SOCIAL_ATTENTION"]["social_influence"]
        logging.info("数据库连接成功")  # jia
        db.insert_one(dict1)
        return "SOCIAL_ATTENTION", "social_influence"
    except Exception as e:   # jia
        logging.error("数据存入数据库失败：%s" % e)   # jia

    # 5：消息服务接口,通知计算完成，给出存数据的数据库名和集合名，没写
def send_message_api(eventNoticeType, eventState, db_name, collection_name):  # eventNoticeType:通知消息类型说明,值为SOCIAL_INFLUENCE表示社会影响力效能评估；eventState：消息服务状态说明，值为SUCCESSFUL表示执行成功并已完成
    BasePath = 'https://api.antdu.com/event/'
    url = BasePath+'notice'
    logging.info("消息服务接口链接: %s", url)  # jia
    # 消息头指定,指定utf-8编码
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    data = {'eventNoticeType': eventNoticeType, 'eventState': eventState, 'db_name': db_name, 'collection_name': collection_name}
    try:  # jia
        requests.post(url, data=json.dumps(data), headers=headers)
        logging.error("成功通知消息服务接口：%s")  # jia
    except Exception as e:    # jia
        logging.error("通知消息服务接口失败：%s" % e)  # jia


def getdata_fromdb_by_id(topicId):
    logging.info('成功调用读数据库函数')  # jia
    BasePath = 'https://api.antdu.com/jw/'
    url = BasePath + 'data/documents'   # https://api.antdu.com/jw/data/documents
    logging.info('输出数据库接口链接: %s', url)  # jia
    endTime = int(round(time.time() * 1000))
    startTime = endTime-86700   # 86400是往前一天，为避免前面调数据有时延，时间往前5分钟
    # startTime = 161509171800
    # endTime = 1615523719551  # 这两个时间是测试时间
    # data = {"topic": topicId, 'startTime': 161509171955, "endTime": time1, "count": 100}
    data = {
        'topic': topicId,
        'startTime': startTime,
        'endTime': endTime,
        'count': 100
    }

    logging.info('向数据库发送请求获取数据')  # jia
    # 向数据库发送请求获取数据
    try:
        c = 1  # jia
        data = requests.get(url, params=data)
        data = json.loads(data.text)
        logging.info("数据库第 %s 次请求成功", c)  # jia
        # print(data)
        numFound = data["numFound"]  # 事件数据库里一共有这么多条数据，根据该数据判断要读多少次
        print(numFound)
        result_list = data["result"]  # 该列表里存放字典，一个字典代表一条数据
        # print(len(result_list))
        endTime = result_list[-1]["createdAt"]
        count = 100
        print("endTime: ", endTime)
        logging.info("数据库本次请求得到数据")  # jia
        # print(result_list)
        for i in range(int(numFound / count)):  # 读事件库的全部数据存到result_list列表里
            c += 1  # jia
            data2 = {"topic": topicId, 'startTime': startTime, "endTime": endTime, "count": count}
            data2 = requests.get(url, params=data2)
            # print("data2.url:", data2.url)
            data2 = json.loads(data2.text)
            logging.info("数据库第 %s 次请求成功", c)  # jia
            logging.info("数据库本次请求得到的数据")  # jia
            # print(data2)
            # print(data2["result"])
            result_list = result_list + data2["result"][1:]  # 该列表里存放字典，一个字典代表一条数据
            # print(len(result_list))
            endTime = result_list[-1]["createdAt"]
        print(len(result_list))
        logging.info("数据库数据读取完毕,接下来是影响力计算")  # jia

        # 3：影响力计算
        dict1 = event_influence_calculate(result_list)
        logging.info("影响力计算结束，数据输出")  # jia
        print(dict1)

        # 4：将计算结果存入数据库
        logging.info("数据准备存入数据库...")  # jia
        db_name, collection_name = save_to_db(dict1)
        logging.info("数据已全部存入数据库,准备连接并通知消息服务，计算完成")  # jia

        # 5：消息服务接口,通知计算完成,给出存数据的数据库名和集合名:接口
        send_message_api('SOCIAL_INFLUENCE', 'SUCCESSFUL', db_name, collection_name)

    except Exception as e:
        logging.error("数据库请求异常：%s" % e)  # gai
        # data = None
        # return data


# 1、消息服务接口,接收数据导入成功的通知
# 接收消息
@app.route('/notice', methods=['post'])  # url = 'http://127.0.0.1:8088/notice',请求方式post
def add_stu():
    try:
        logging.info('接口被调用成功')  # jia
        if not request.data:  # 检测是否有数据
            logging.info('未检测到数据')  # jia
            return ('fail')
        data = request.data.decode('utf-8')
        # 获取到POST过来的数据，因为我这里传过来的数据需要转换一下编码。根据具体情况而定
        data_json = json.loads(data)
        # 把区获取到的数据转为JSON格式。
        logging.info('接收到的数据：%s', data_json)
        # print(data_json)
        eventNoticeType = data_json["eventNoticeType"]  # 获取通知消息类型说明：SOCIAL_INFLUENCE为社会影响力效能评估
        eventState = data_json["eventState"]  # 获取消息服务状态说明：SUCCESSFUL为执行成功并已完成
        topicId = data_json["topicId"]  # 获取关联主题id
        if eventNoticeType == 'SOCIAL_INFLUENCE' and eventState == 'SUCCESSFUL':
            logging.info('调用读数据库函数')  # jia
            getdata_fromdb_by_id(topicId)  # 如果接收到 数据全部入库 的消息，则根据通知接口拿到的事件ID（topicId）去调用接口3.2.1.3，获取我们需要的数据

        return jsonify(data_json)
        # 返回JSON数据。
    except Exception as e:
        logging.error("接口被调用失败：%s" % e)


# 创建主函数
if __name__ == '__main__':
    # 1：消息服务接口,接收数据导入成功的通知:接口
    # app.run(host='0.0.0.0', port=8088)    # url = 'http://127.0.0.1:8088/notice'
    server = pywsgi.WSGIServer(('0.0.0.0', 8088), app)
    server.serve_forever()
    # 这里指定了地址和端口号。
    # timer = threading.Timer(5, do_job)
    # timer.start()
