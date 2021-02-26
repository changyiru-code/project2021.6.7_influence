import json
import requests
import logging
import threading
import time

from flask import Flask, request, jsonify
app = Flask(__name__)
app.debug = True

# 2：连接数据库，得到集合数据，数据库访问接口，要改接口
# 收到通知后，以事件id作为参数调用提供的一个事件关联数据查询接口翻页查询事件关联的数据进行事件影响力分析。
# 怎么通过id访问，目前是通过数据库名和集合名读取数据
# 通过ID读数据库数据

def getdata_fromdb_by_id(topicId):
    BasePath = 'https://api.antdu.com/jw/'
    url = BasePath+'data/douments'
    time1 = int(time.time())
    data = {"topicId": topicId, "endTime": time1, "count": 100}
    # 向数据库发送请求获取数据
    try:
        data = requests.get(url, params=data)
        data = json.loads(data)
        numFound = data["numFound"]  # 事件数据库里一共有这么多条数据，根据该数据判断要读多少次
        result_list = data["result"]   # 该列表里存放字典，一个字典代表一条数据
        endTime = result_list[-1]["createdAt"]
        count = 100
        for i in range(int(numFound/count)):  # 读事件库的全部数据存到result_list列表里
            data2 = {"topicId": topicId, "endTime": endTime, "count": count}
            data2 = requests.get(url, params=data2)
            data2 = json.loads(data2)
            result_list = result_list + data2["result"]   # 该列表里存放字典，一个字典代表一条数据
            endTime = result_list[-1]["createdAt"]


    except Exception as e:
        logging.error("请求异常：%s" % e)
        data = None
    return data

# 1：消息服务接口,接收数据导入成功的通知，没写
#     参考接收消息部分：https://www.php.cn/python-tutorials-424691.html
# 接收消息

@app.route('/get/data/', methods=['post'])
def add_stu():
    if not request.data:  # 检测是否有数据
        return ('fail')
    data = request.data.decode('utf-8')
    # 获取到POST过来的数据，因为我这里传过来的数据需要转换一下编码。根据晶具体情况而定
    data_json = json.loads(data)
    # 把区获取到的数据转为JSON格式。
    print(data_json)
    eventNoticeType = data_json["eventNoticeType"]
    eventState = data_json["eventState"]
    topicId = data_json["topicId"]
    if eventNoticeType == 'SOCIAL_INFLUENCE' and eventState == 'SUCCESSFUL':
        getdata_fromdb_by_id(topicId)  # 如果接收到 数据全部入库 的消息，则根据通知接口拿到的事件ID（topicId）去调用接口3.2.1.3，获取我们需要的数据

    return jsonify(data_json)
    # 返回JSON数据。





if __name__ == '__main__':
    app.run(host='127.0.0.1', port=1234)
    # 这里指定了地址和端口号。
    # timer = threading.Timer(5, do_job)
    # timer.start()



#     # 5：消息服务接口,通知计算完成，给出存数据的数据库名和集合名
# def send_message_api(eventNoticeType, eventState):  # eventNoticeType:通知消息类型说明,值为SOCIAL_INFLUENCE表示社会影响力效能评估；eventState：消息服务状态说明，值为SUCCESSFUL表示执行成功并已完成
#     BasePath = 'https://api.antdu.com/event/'
#     url = BasePath+'notice'
#     # 消息头指定,指定utf-8编码
#     headers = {'Content-Type': 'application/json;charset=UTF-8'}
#     data = {'eventNoticeType': eventNoticeType, 'eventState': eventState}
#     requests.post(url, data=json.dumps(data), headers=headers)
