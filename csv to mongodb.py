#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2021/2/22
# @Author  : yiru Chang
# @Site   :
# @File   : csv文件存入mongoDB(csv to mongodb.py)
# @Software  : PyCharm

# 导包
from pymongo import MongoClient
import csv
# 创建连接MongoDB数据库函数
def connection():
    # 1:账号密码方式连接本地MongoDB数据库服务 | "mongodb://用户名:密码@公网ip:端口/"
    conn = MongoClient("mongodb://root:19980529@127.0.0.1:27017/")  # 用户名、密码可修改
    # 2:连接本地数据库(influence)。没有时会自动创建
    db = conn.influence
    # 3:创建集合
    set1 = db.keyword3_status
    # # 4:看情况是否选择清空(两种清空方式，第一种不行的情况下，选择第二种)
    # #第一种直接remove
    # set1.remove(None)
    # #第二种remove不好用的时候
    # # set1.delete_many({})
    return set1
def insertToMongoDB(set1):
    # 打开文件guazi.csv
    with open('D:\my_file\研究生期间的资料\影响力评价模型-参考论文\司法案件影响力评估-项目\data-all\data-all\status\status-by-keyword\keyword3-status.csv', 'r', encoding='utf-8')as csvfile:
        # 调用csv中的DictReader函数直接获取数据为字典形式
        reader = csv.DictReader(csvfile)
        # 创建一个counts计数一下 看自己一共添加了了多少条数据
        counts = 0
        for each in reader:
            # 将数据中需要转换类型的数据转换类型。原本全是字符串（string）。
            each['repostsCount']=int(each['repostsCount'])  # 将字符串转换成int型存储
            # each['价格']=float(each['价格'])
            # each['原价']=float(each['原价'])
            each['commentsCount']=int(each['commentsCount'])  # 将字符串转换成int型存储
            # each['表显里程']=float(each['表显里程'])
            # each['排量']=float(each['排量'])
            # each['过户数量']=int(each['过户数量'])
            set1.insert(each)
            counts += 1
            print('成功添加了'+str(counts)+'条数据 ')


# 创建主函数
def main():
    set1 = connection()
    insertToMongoDB(set1)


main()




