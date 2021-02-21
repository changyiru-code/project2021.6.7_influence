from pymongo import MongoClient
import pprint
# 账号密码方式连接MongoDB | "mongodb://用户名:密码@公网ip:端口/"
client = MongoClient("mongodb://root:19980529@127.0.0.1:27017/")  # 用户名、密码可修改

# 指定数据库
db = client.test   # test是数据库名称，可修改

# 指定集合
collection = db.students  # students是集合名称，可修改

# # 插入数据
# student = {'id': '20190101', 'name': 'Tom3', 'age': 20, 'gender': 'female'}
# ret = collection.insert_one(student)  # collection.insert_one()方法 插入文档
# print('insert_id:', ret.inserted_id)  # 插入文档时，如果文档尚未包含“_id”键，则会自动添加“_id”。

# 插入数据
student = {'id': '20190101', 'name': 'Tom3', 'age': 20, 'gender': 'female', 'class': '2001'}
ret = collection.insert_one(student)  # collection.insert_one()方法 插入文档
print('insert_id:', ret.inserted_id)  # 插入文档时，如果文档尚未包含“_id”键，则会自动添加“_id”。


# # 使用find_one()获取单个文档
# pprint.pprint(collection.find_one())  # 返回集合的第一个文档内容
#
# # 使用find_one("key":"value")获取满足条件的一个文档
# pprint.pprint(collection.find_one({"age": "20"}))  # 返回集合中满足条件的一个文档内容


# # 更新数据
# condition = {'name': 'Tom3'}
# edit = {'age': 21}
# ret = collection.update_one(condition, {'$set': edit})
# print('update:', ret.matched_count, ret.modified_count)
#
# # 查询
# info = collection.find_one(condition)
# print('select:', info)
#
# # 计数
# count = collection.count_documents({})
# print('count:', count)
#
# # 删除数据
# ret = collection.delete_one(condition)
# print('delete:', ret.deleted_count)
