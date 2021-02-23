# # 将汉字年月日转为--表示的日期
# import time
# publish_Time = "2018年10月10日"
# array = time.strptime(publish_Time, u"%Y年%m月%d日")
# print(array)
# try:
#     publishTime = time.strftime("%Y-%m-%d", array)
# except Exception as e:
#     print(e)
# print(publishTime)
import csv
path='D:\my_file\研究生期间的资料\影响力评价模型-参考论文\司法案件影响力评估-项目\data-all\data-all\status\status-by-keyword\keyword1-status.csv'
# with open(path, 'r', encoding='utf-8') as csvfile:
#     reader = csv.reader(csvfile)
#     mod_times = [row[3] for row in reader]  # 提取每一行的时间
# print(mod_times)
# for x in mod_times[1:]:
#     print(x)


with open(path, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    mod_times = [row['createAt'] for row in reader]
print(mod_times)