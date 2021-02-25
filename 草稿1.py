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
# url = 'https://api.github.com/events'
#
# r = requests.get(url)
# print(json.loads(r.text))   #r.json()与json.loads(r.text)等效
# print(r.json())  #这两个print语句等效
