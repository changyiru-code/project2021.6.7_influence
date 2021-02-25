import json
import requests
import logging
import threading
# 2：连接数据库，得到集合数据，数据库访问接口，要改接口
# 收到通知后，以事件id作为参数调用提供的一个事件关联数据查询接口翻页查询事件关联的数据进行事件影响力分析。
# 怎么通过id访问，目前是通过数据库名和集合名读取数据

def getdata_fromdb_by_id(topicId):
    BasePath = 'https://api.antdu.com/jw/'
    url = BasePath+'data/douments'
    data = {"topicId": topicId}

    # 向数据库发送请求获取数据
    try:
        data = requests.get(url, params=data)
        json.loads(data)
    except Exception as e:
        logging.error("请求异常：%s" % e)
        data = None
    return data



# 1：消息服务接口,接收数据导入成功的通知，没写
#     参考接收消息部分：https://www.php.cn/python-tutorials-424691.html
# 接收消息
def accept_msg():
    BasePath = 'https://api.antdu.com/event/'
    url = BasePath+'notice'
    # 消息头指定,指定utf-8编码
    headers = {'Content-Type': 'application/json;charset=UTF-8'}

    try:
        meg = requests.post(url, headers=headers)
        eventNoticeType = meg.json().get("eventNoticeType")
        eventState = meg.json().get("eventState")
        topicId = meg.json().get("topicId")
        if eventNoticeType == 'SOCIAL_INFLUENCE' and eventState == 'SUCCESSFUL':
            getdata_fromdb_by_id(topicId)  # 如果接收到 数据全部入库 的消息，则根据通知接口拿到的事件ID（topicId）去调用接口3.2.1.3，获取我们需要的数据
        else:
            timer = threading.Timer(5, accept_msg)
            timer.start()

    except Exception as e:
        print(e)


def main():
    accept_msg()
    # timer = threading.Timer(5, do_job)
    # timer.start()


main()

#     # 5：消息服务接口,通知计算完成，给出存数据的数据库名和集合名，没写
# def send_message_api(eventNoticeType, eventState):  # eventNoticeType:通知消息类型说明,值为SOCIAL_INFLUENCE表示社会影响力效能评估；eventState：消息服务状态说明，值为SUCCESSFUL表示执行成功并已完成
#     BasePath = 'https://api.antdu.com/event/'
#     url = BasePath+'notice'
#     # 消息头指定,指定utf-8编码
#     headers = {'Content-Type': 'application/json;charset=UTF-8'}
#     data = {'eventNoticeType': eventNoticeType, 'eventState': eventState}
#     requests.post(url, data=json.dumps(data), headers=headers)
