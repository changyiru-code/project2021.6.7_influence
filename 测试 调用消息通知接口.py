##2每次测试正确代码都用这个
import requests, json
import logging
    # 5：消息服务接口,通知计算完成，给出存数据的数据库名和集合名，没写
def send_message_api(eventNoticeType, eventState, db_name, collection_name, topicId):  # eventNoticeType:通知消息类型说明,值为SOCIAL_INFLUENCE表示社会影响力效能评估；eventState：消息服务状态说明，值为SUCCESSFUL表示执行成功并已完成
    BasePath = 'https://api.antdu.com/event/'
    url = BasePath+'notice/'
    logging.info("消息服务接口链接: %s", url)  # jia
    # 消息头指定,指定utf-8编码
    # data = {'eventNoticeType': eventNoticeType, 'eventState': eventState, 'db_name': db_name, 'collection_name': collection_name}
    # noticeCotent = {'db_name': db_name, 'collection_name': collection_name}
    # noticeCotent = json.dumps(noticeCotent)
    # data = {'noticeType': {
    #     'notices': {'eventNoticeType': eventNoticeType, 'eventState': eventState, 'noticeCotent': noticeCotent}
    # }}
    data = {'noticeType': eventNoticeType, 'eventState': eventState, 'db_name': db_name, 'collection_name': collection_name, 'topicId': topicId}

    try:  # jia
        r = requests.post(url, data=data)
        print(r.text)
        logging.info("成功通知消息服务接口：%s", r.text)  # jia
    except Exception as e:    # jia
        logging.error("通知消息服务接口失败：%s" % e)  # jia


db_name = "SOCIAL_ATTENTION"
collection_name = 'social_influence'
topicId = 'ff557982-43d8-4256-a256-0d0854ef114a'
# 5：消息服务接口,通知计算完成,给出存数据的数据库名和集合名:接口
send_message_api('SOCIAL_INFLUENCE', 'SUCCESSFUL', db_name, collection_name, topicId)
