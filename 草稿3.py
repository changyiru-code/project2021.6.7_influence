# # 导包
# from pymongo import MongoClient
# import pandas as pd
# import numpy as np
# from datetime import datetime
# import json
# from bson import ObjectId
# import json
#
#
# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)
#
#
# # 创建连接MongoDB数据库函数
# def connection():
#     resu = {
#         "﻿docid": "si4587134696823542",
#         "platform": "sina",
#         "contentId": "4587134696823542",
#         "createAt": "2020-12-28 15:46:10",
#         "title": "",
#         "content": "#百香果女孩案凶手再审被改判死刑#\n自从知道这个案子每次买百香果吃百香果的时候都会隐隐难受。虽然结果大快人心，但看了女孩母亲的采访视频，开心不起来。哭得撕心裂肺说''女儿可以入土为安了。但不管怎样都换不回我女儿！''凶手毁灭的是一个家庭。从案发到再审宣判这两年多，这个家庭得多绝望无助。...全文： http://weibo.com/5830819541/JAyLPsD78",
#         "originalContent": "",
#         "stateType": "0.0",
#         "retweetId": "-1",
#         "retweetUserId": "",
#         "retweetUserName": "",
#         "replyStatusId": "-1",
#         "replyUserId": "",
#         "replyUserName": "",
#         "url": "http://weibo.com/5830819541/JAyLPsD78",
#         "picUrl": "",
#         "audioUrl": "",
#         "latitude": "0.0",
#         "longitude": "0.0",
#         "userId": "5830819541",
#         "location": "海外",
#         "userName": "--白衣卿相",
#         "nickName": "--白衣卿相",
#         "userHead": "https://tva2.sinaimg.cn/crop.0.0.996.996.50/006mBwwtjw8f9bx9bhqjej30ro0rojsz.jpg?KID=imgbed,tva&Expires=1609152400&ssig=i6YRbyNlJS",
#         "vip": "False",
#         "vipType": "-1",
#         "repostsCount": 0,
#         "commentsCount": 0,
#         "favourCount": "",
#         "videoUrlList": "",
#         "scope": "",
#         "mediaType": "",
#         "domain": "",
#         "channelName": "",
#         "source": "OPPO随光而变R17",
#         "docType": ""
#     }
#
#     return resu
#
#
#
#
#
# import flask, json
# from flask import request
#
# '''
# flask： web框架，通过flask提供的装饰器@server.route()将普通函数转换为服务
# 登录接口，需要传url、username、passwd
# '''
# # 创建一个服务，把当前这个python文件当做一个服务
# server = flask.Flask(__name__)
#
#
# # server.config['JSON_AS_ASCII'] = False
# # @server.route()可以将普通函数转变为服务 登录接口的路径、请求方式
# @server.route('/accept', methods=['get', 'post'])
# def login():
#
#     # 连接数据库，得到集合数据
#     resu = connection()
#
#     return resu  # 将字典转换为json串, json是字符串
#
# if __name__ == '__main__':
#     server.run(debug=True, port=8888, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
#

import json
import requests


request_param = {
    'topic': 'ff557982-43d8-4256-a256-0d0854ef114a',
    'startTime': 161509171955,
    'endTime': 1615523719551,
    'count': 80
}
r = requests.get('https://api.antdu.com/jw/data/documents', params = request_param)
print(r.url)                       #获取请求内容
print(r.text)                      #获取响应内容
data = json.loads(r.text)
numFound = data["numFound"]  # 事件数据库里一共有这么多条数据，根据该数据判断要读多少次
print(numFound)
print(data)
