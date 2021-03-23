"""对social_influence.py的读数据库部分的调试，应该没问题了"""
# # 模型第三步，读取mongodb数据库，只读取一个事件，时间以时为单位，运行公式模型，计算单独一个事件的影响力，输出结果格式为字典，进行归一化
# 读取数据库里的测试数据，验证模型
# 存入数据库

# 导包
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
app = Flask(__name__)
app.debug = True
from gevent import pywsgi
logging.basicConfig(level=logging.DEBUG)  # jia


# 通过ID读数据库数据
# 2：连接数据库，得到集合数据，数据库访问接口，要改接口
# 收到通知后，以事件id作为参数调用提供的一个事件关联数据查询接口翻页查询事件关联的数据进行事件影响力分析。
# 怎么通过id访问，目前是通过数据库名和集合名读取数据
# 通过ID读数据库数据
def getdata_fromdb_by_id(topicId):

    print('aaa')

# 1、消息服务接口,接收数据导入成功的通知
# 接收消息
@app.route('/notice', methods=['post'])  # url = 'http://127.0.0.1:8088/notice',请求方式post
def add_stu():
    try:  # jia
        logging.info('接口被调用成功')  # jia
        logging.info('接收到的数据：%s', request.values)    # jia
        # 获取通过url请求传参的数据
        noticeType = request.values.get('eventNoticeType')
        eventState = request.values.get('eventState')
        topicId = request.values.get('topicId')
        # 判断状态、类型、id都不为空
        if noticeType and eventState and topicId:
            if noticeType == 'SOCIAL_INFLUENCE' and eventState == 'SUCCESSFUL':
                logging.info('调用读数据库函数')  # jia
                getdata_fromdb_by_id(topicId)  # 如果接收到 数据全部入库 的消息，则根据通知接口拿到的事件ID（topicId）去调用接口3.2.1.3，获取我们需要的数据
                return 'true'
            else:
                logging.info('发送的消息不对')  # jia
                resu = {'code': -1, 'message': '类型或状态不对'}
                return json.dumps(resu, ensure_ascii=False)
        else:
            resu = {'code': 10001, 'message': '未检测到数据or参数不能为空！'}
            return json.dumps(resu, ensure_ascii=False)
        # 返回JSON数据。
    except Exception as e:  # jia
        logging.error("接口被调用失败：%s" % e)  # jia


# 创建主函数
if __name__ == '__main__':
    # 1：消息服务接口,接收数据导入成功的通知:接口
    # app.run(host='0.0.0.0', port=8088)    # url = 'http://127.0.0.1:8088/notice'
    server = pywsgi.WSGIServer(('0.0.0.0', 8088), app)
    server.serve_forever()
    # 这里指定了地址和端口号。
    # timer = threading.Timer(5, do_job)
    # timer.start()


