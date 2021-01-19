"""
python读取csv文件实现熵权法
输入：csv文件
输出：权值
"""
import pandas as pd
import numpy as np
import copy

from numpy import array
# 定义熵值法函数
def cal_weight(x):
    '''熵值法计算变量的权重'''
    fenshu = copy.deepcopy(x)
    # 标准化
    fenshu = fenshu.apply(lambda fenshu: ((fenshu - np.min(fenshu)) / (np.max(fenshu) - np.min(fenshu))))
    print(fenshu)
    # 求k
    rows = fenshu.index.size  # 行
    print(rows)
    k = 1.0 / np.log(rows)
    yij = (1 + fenshu).sum(axis=0)
    # 第二步，计算pij
    pij = (1 + fenshu) / yij
    # print(pij)
    test = pij * np.log(pij)
    test = np.nan_to_num(test)
    # print(test)
    # 计算每种指标的信息熵
    ej = -k * (test.sum(axis=0))
    # 计算每种指标的权重
    w = (1 - ej) / np.sum(1 - ej)
    print('w:', w)
    print(w)
    print(x)
    add_wi=x*w
    print(add_wi)
    score=add_wi.sum(axis=1)
    print(score)
    # return w
    
def main():
    # 1读取数据
    df = pd.read_csv('D:\\influence_el\\shangquan.csv', encoding='utf-8')
    # df.to_excel('D:\\influence_el\\shangquan1.xlsx')  #将csv文件转成xlsx文件，这里不需要转
    # 2数据预处理 ,去除空值的记录
    df.dropna()
    # 去掉“微博”这个指标
    df.drop(columns="微博", axis=1, inplace=True)
    print(df)
    cal_weight(df)
    # # 计算df各字段的权重
    # w = cal_weight(df)  # 调用cal_weight
    #
    # w.index = df.columns
    # w.columns = ['weight']
    # print(w)
    # print('运行完成!')
main()
# 不修饰pij的结果
# A  0.075786
# B  0.219159
# C  0.271374
# D  0.065592
# E  0.105198
# F  0.065592
# G  0.066116
# H  0.065592
# I  0.065592
# 修饰pij的结果
# A  0.090926
# B  0.214447
# C  0.208902
# D  0.077984
# E  0.095937
# F  0.077984
# G  0.077852
# H  0.077984
# I  0.077984