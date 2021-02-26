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



# ##2
# import requests, json
#
# data = {
#     'id': 1,
#     'name': 'lily',
#     'age': 12,
#     'birthplace': 'san',
#     'grade': 123
# }
# url = 'http://127.0.0.1:1234/get/data/'
#
# requests.post(url, data=json.dumps(data))
#
