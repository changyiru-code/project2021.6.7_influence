# -*- coding: utf-8 -*-
"""
python读取excel文件实现熵权法
输入：excel文件
输出：各对象的得分
"""
import numpy as np
import pandas as pd
import copy

def cal_weight(m,data):
    fenshu = copy.deepcopy(data)
    print(fenshu)
    print(type(fenshu))
    #标准化
    #正指标 (x-min)/(max-min)
    # 负指标 (max-x)/(max-min)
    for i in list(fenshu.columns):
       # 获取各个指标的最大值和最小值
        Max = np.max(fenshu[i])
        Min = np.min(fenshu[i])
       # 标准化
        fenshu[i] = (fenshu[i] - Min) / (Max - Min)
    # print(fenshu)
    k=1/np.log(m)
    yij=(1+fenshu).sum(axis=0)
    #第二步，计算pij
    pij=(1+fenshu)/yij

    # print(pij)
    test=pij*np.log(pij)
    test=np.nan_to_num(test)
    # print(test)
    #计算每种指标的信息熵
    ej=-k*(test.sum(axis=0))
    #计算每种指标的权重
    wi=(1-ej)/np.sum(1-ej)
    print('wi:',wi)
    print(type(wi))
    print(data)
    # 计算得分/评分
    wi_dataframe= pd.DataFrame(wi)
    print(type(wi_dataframe))
    add_wi=data*wi
    print(add_wi)
    score=add_wi.sum(axis=1)
    print(score)

def main():
    fp = "D:\\influence_el\\shangquan1.xlsx"
    data = pd.read_excel(fp)
    m, n = data.shape
    data.drop(columns="科室", axis=1, inplace=True)  # 去掉“科室”这个指标
    cal_weight(m,data)
main()

# wi: [0.09092611 0.21444689 0.20890223 0.07798402 0.09593719 0.07798402
#  0.07785151 0.07798402 0.07798402]