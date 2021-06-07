from pymongo import MongoClient
def save_to_db(dict1, topicId):
    # 1:账号密码方式连接本地MongoDB数据库服务 | "mongodb://用户名:密码@公网ip:端口/"
    conn = MongoClient("mongodb://root:19980529@127.0.0.1:27017/")  # 用户名、密码可修改
    # 2:连接本地分析结果数据库(influence)和集合(event_influence)
    db = conn["influence_result"]['event_influence']
    db.update_one(
        {'case_id': topicId},
        {'$set':
            dict1
        },
        upsert=True
    )
    # db.insert_one(dict1)


# 创建主函数
def main():
    d1 = {'case_id': '86d6619e-8209-4ec3-bae9-b6086e8d93ef', 'result': [
        {'topic_influence': 89.04970896842251, 'user_engage': 92.29148068598761, 'topic_coverage': 92.37480832877279,
         'topic_activity': 97.70672842987298, 'topic_novelty': 34.69785659411364,
         'topic_persistence': 87.45955868928102}]}
    d2 = {'case_id': '76d6619e-8209-4ec3-bae9-b6086e8d93ef', 'result': [
        {'topic_influence': 1.04970896842251, 'user_engage': 92.29148068598761, 'topic_coverage': 92.37480832877279,
         'topic_activity': 97.70672842987298, 'topic_novelty': 34.69785659411364,
         'topic_persistence': 87.45955868928102}]}
    d3 = {'case_id': '26d6619e-8209-4ec3-bae9-b6086e8d93ef', 'result': [
        {'topic_influence': 2.04970896842251, 'user_engage': 92.29148068598761, 'topic_coverage': 92.37480832877279,
         'topic_activity': 97.70672842987298, 'topic_novelty': 34.69785659411364,
         'topic_persistence': 87.45955868928102}]}

    # 4：将计算结果存入数据库
    save_to_db(d2, '76d6619e-8209-4ec3-bae9-b6086e8d93ef')


main()
