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
#     resu = {'code': 200, 'message': '登录成功'}
#     return json.dumps(resu, ensure_ascii=False)  # 将字典转换为json串, json是字符串
#
# if __name__ == '__main__':
#     server.run(debug=True, port=8888, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问



##2每次测试正确代码都用这个
import requests, json
data = {
    'eventNoticeType': 'SOCIAL_INFLUENCE',
    'eventState': 'SUCCESSFUL',
    'topicId': 'ff557982-43d8-4256-a256-0d0854ef114a',
}
url = 'http://10.20.2.181:8088/notice'  # http://10.20.2.181:8088/notice
# http://127.0.0.1:8088/notice
r = requests.post(url, data=json.dumps(data))
print(r.text)

# # #测试post方式没问题
# import json
# import logging
#
# import requests
# logging.basicConfig(level=logging.DEBUG)
#
#
#
#     # 5：消息服务接口,通知计算完成，给出存数据的数据库名和集合名，没写
# def send_message_api():  # eventNoticeType:通知消息类型说明,值为SOCIAL_INFLUENCE表示社会影响力效能评估；eventState：消息服务状态说明，值为SUCCESSFUL表示执行成功并已完成
#     url = 'http://127.0.0.1:8088/notice'
#     logging.info("消息服务接口链接: %s", url)  # jia
#     # 消息头指定,指定utf-8编码
#     # headers = {'Content-Type': 'application/json;charset=UTF-8'}
#     data = {
#         'eventNoticeType': 'SOCIAL_INFLUENCE',
#         'eventState': 'SUCCESSFUL',
#         'topicId': 'ff557982-43d8-4256-a256-0d0854ef114a',
#     }
#     try:  # jia
#         r = requests.post(url, data=json.dumps(data))
#         # r = requests.post(url, data=json.dumps(data), headers=headers)
#         print(r.text)
#         logging.info("成功通知消息服务接口")  # jia
#     except Exception as e:    # jia
#         logging.error("通知消息服务接口失败：%s" % e)  # jia
#
#
# def getdata_fromdb_by_id():
#     # 5：消息服务接口,通知计算完成,给出存数据的数据库名和集合名:接口
#     # send_message_api('SOCIAL_INFLUENCE', 'SUCCESSFUL', db_name, collection_name)
#     send_message_api()
#
#
# # 创建主函数
# if __name__ == '__main__':
#     getdata_fromdb_by_id()
#
