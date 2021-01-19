##模型第二步，python 读取mysql写入csv文件
import pandas as pd
import pymysql
conn = pymysql.connect(host='localhost', user='root', passwd='19980529', db='influence', charset='utf8')
sql = "select * from huati0"
df = pd.read_sql(sql, con=conn)
df.to_csv("D:\\常艺茹的文档\\研究生期间的资料\\影响力评价模型-参考论文\\data\\huati0.csv")
sql = "select * from huati1"
df = pd.read_sql(sql, con=conn)
df.to_csv("D:\\常艺茹的文档\\研究生期间的资料\\影响力评价模型-参考论文\\data\\huati1.csv")
sql = "select * from huati2"
df = pd.read_sql(sql, con=conn)
df.to_csv("D:\\常艺茹的文档\\研究生期间的资料\\影响力评价模型-参考论文\\data\\huati2.csv")
sql = "select * from huati3"
df = pd.read_sql(sql, con=conn)
df.to_csv("D:\\常艺茹的文档\\研究生期间的资料\\影响力评价模型-参考论文\\data\\huati3.csv")
sql = "select * from huati4"
df = pd.read_sql(sql, con=conn)
df.to_csv("D:\\常艺茹的文档\\研究生期间的资料\\影响力评价模型-参考论文\\data\\huati4.csv")
sql = "select * from huati5"
df = pd.read_sql(sql, con=conn)
df.to_csv("D:\\常艺茹的文档\\研究生期间的资料\\影响力评价模型-参考论文\\data\\huati5.csv")
sql = "select * from huati6"
df = pd.read_sql(sql, con=conn)
df.to_csv("D:\\常艺茹的文档\\研究生期间的资料\\影响力评价模型-参考论文\\data\\huati6.csv")
sql = "select * from huati7"
df = pd.read_sql(sql, con=conn)
df.to_csv("D:\\常艺茹的文档\\研究生期间的资料\\影响力评价模型-参考论文\\data\\huati7.csv")
sql = "select * from huati8"
df = pd.read_sql(sql, con=conn)
df.to_csv("D:\\常艺茹的文档\\研究生期间的资料\\影响力评价模型-参考论文\\data\\huati8.csv")
sql = "select * from huati9"
df = pd.read_sql(sql, con=conn)
df.to_csv("D:\\常艺茹的文档\\研究生期间的资料\\影响力评价模型-参考论文\\data\\huati9.csv")
conn.close()



