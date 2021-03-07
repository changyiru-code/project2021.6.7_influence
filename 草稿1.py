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


import json
from flask import Flask, request, jsonify
app = Flask(__name__)
app.debug = True

def getdata_fromdb_by_id(topicId):
    print(topicId)
# 1、消息服务接口,接收数据导入成功的通知
# 接收消息
@app.route('/notice', methods=['post'])  # url = 'http://127.0.0.1:8088/notice',请求方式post
def add_stu():
    if not request.data:  # 检测是否有数据
        return ('fail')
    data = request.data.decode('utf-8')
    # 获取到POST过来的数据，因为我这里传过来的数据需要转换一下编码。根据具体情况而定
    data_json = json.loads(data)
    # 把区获取到的数据转为JSON格式。
    print(data_json)
    eventNoticeType = data_json["eventNoticeType"]  # 获取通知消息类型说明：SOCIAL_INFLUENCE为社会影响力效能评估
    eventState = data_json["eventState"]  # 获取消息服务状态说明：SUCCESSFUL为执行成功并已完成
    topicId = data_json["topicId"]  # 获取关联主题id
    if eventNoticeType == 'SOCIAL_INFLUENCE' and eventState == 'SUCCESSFUL':
        getdata_fromdb_by_id(topicId)  # 如果接收到 数据全部入库 的消息，则根据通知接口拿到的事件ID（topicId）去调用接口3.2.1.3，获取我们需要的数据

    return jsonify(data_json)
    # 返回JSON数据。

# 创建主函数
if __name__ == '__main__':
    # 1：消息服务接口,接收数据导入成功的通知:接口
    app.run(host='0.0.0.0', port=8088)    # url = 'http://127.0.0.1:8088/notice'
    # 这里指定了地址和端口号。
    # timer = threading.Timer(5, do_job)
    # timer.start()
