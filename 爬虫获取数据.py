# -*- coding: utf-8 -*-
#模型第一步，爬数据，存到mysql
from urllib import parse
import requests
from bs4 import BeautifulSoup
import re
import jieba
import time
import pymysql

def fenci(document):
    cut_words = jieba.cut(document)
    return list(cut_words)
def qutingyongci(contents, stopwords):
    contents_clean = []
    for line in contents:
        line_clean = []
        for word in line:
            if word in stopwords:
                continue
            line_clean.append(word)
        contents_clean.append(line_clean)
    return contents_clean
def qu(result,subTextHead,subTextFoot,stpwrdlst):
    resultExcel1 = re.sub(subTextHead, '', result)
    zanshu = re.sub(subTextFoot, '', resultExcel1)
    zan_list1_document_cut = fenci(zanshu)
    zan_list1_document_cut_qutingyongci = qutingyongci(zan_list1_document_cut, stpwrdlst)
    zan_result = []
    for line in zan_list1_document_cut_qutingyongci:
        zan_result1 = ''.join(line)
        zan_result.append(zan_result1)
    return zan_result
def zhixing(sql):
    db = pymysql.connect(host='localhost', user='root', passwd='19980529', db='influence', charset='utf8')
    cusor=db.cursor()
    try:
        cusor.execute(sql)
        db.commit()  # 提交到数据库
    except Exception as e:  # 获取报错信息
        print(e)
    db.close()
def create_db():
    sql='create table huati7(xuhao int primary key auto_increment,author varchar(128),content text,zan varchar(256),zhuanfa varchar(256),pinglun varchar(256),public_time varchar(128))'
    zhixing(sql)
def insert_db(sql,list1_result):
    for list_result in list1_result:
        print(list_result)
        db = pymysql.connect(host='localhost', user='root', passwd='19980529', db='influence', charset='utf8')  # db为所使用的数据库
        cusor = db.cursor()
        try:
            cusor.execute(sql, list_result)
            db.commit()
        except Exception as e:
            print(e)
        db.close()


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Host': 'weibo.cn',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': '__guid=78840338.103636774825205200.1597377764281.5493; _T_WM=5e16b39b4abf5a97fbbc17e1ee848130; SCF=Akpp0O77sioU81wRet3azZOPwqjd-Qlz99wcgsq0GH1Bsw4And7qpFj8BAKCaRKQ7ctGGEn-EvX81T9zMCmr2Ko.; SUB=_2A25yhsyBDeRhGeBK7lEW-SfMwzWIHXVRiNTJrDV6PUJbktANLRnmkW1NR4nLGTI8DRwAETV4UFIKkFJy_2EKFYMy; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFiuvFKOj8PSKhkj2nkT_uk5JpX5K-hUgL.FoqXSKeN1K.71h.2dJLoI0YLxKBLBonL1h5LxKML1KBL1-qLxKML1hnLBo2LxKqL1-BLBo5LxKqLBo5LBonLxKBLBonL12BLxK-L12qL1Knt; SUHB=0d4udf7ePfpwbe; SSOLoginState=1602403537; ALF=1604995537; monitor_count=220',
        'DNT': '1',
        'Connection': 'keep-alive'
    }
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError as e:
        print('抓取错误', e.args)

# find hot search from weibo by keyword
def parse_html(html,list1_result):
    soup = BeautifulSoup(html, 'lxml')
    li0 = []
    namelists = soup.find_all('a', attrs={'class': 'nk'})
    for namelist in namelists:
        name = namelist.string
        li0.append(name)
    li1=[]
    contentlists = soup.find_all('span', attrs={'class': 'ctt'})
    for contentlist in contentlists:
        infos = []
        info = list(contentlist.stripped_strings)
        infos.append(info)
        for list1 in infos:
            corpus_str_join = ''.join(list1)
        li1.append(corpus_str_join)
    subTextHead = re.compile(">")
    subTextFoot = re.compile("<")
    stpwrdpath = '去赞、评论、转发停用词表.txt'
    stpwrd_dic = open(stpwrdpath, 'r', encoding='utf-8')
    stpwrd_content = stpwrd_dic.read()
    stpwrdlst = stpwrd_content.splitlines()
    li2=[]
    pattern1 = re.compile('<a href="https://weibo.cn/attitude.*?">.*?</a>')
    zanlists = re.findall(pattern1, html)
    for zanlist in zanlists:
        zan = str(zanlist)
        zanResults = re.findall(">.*?<", zan)
        for result in zanResults:
            zan_result = qu(result, subTextHead, subTextFoot, stpwrdlst)
        li2.append(zan_result[2])
    li3=[]
    pattern1 = re.compile('<a href="https://weibo.cn/repost.*?">.*?</a>')
    zhuanfalists = re.findall(pattern1, html)
    for zhuanfalist in zhuanfalists:
        zhuanfa = str(zhuanfalist)
        zhuanfaResults = re.findall(">.*?<", zhuanfa)
        for result in zhuanfaResults:
            zhuanfa_result = qu(result, subTextHead, subTextFoot, stpwrdlst)
        li3.append(zhuanfa_result[2])
    li4=[]
    pattern1 = re.compile('<a href="https://weibo.cn/comment.*?">.*?</a>')
    pinglunlists = re.findall(pattern1, html)
    for pinglunlist in pinglunlists:
        pinglun = str(pinglunlist)
        pinglunResults = re.findall(">.*?<", pinglun)
        for result in pinglunResults:
            pinglun_result = qu(result, subTextHead, subTextFoot, stpwrdlst)
            if pinglun_result[2]!='':
                li4.append(pinglun_result[2])
    li5=[]
    pubtimelists = soup.find_all('span', attrs={'class': 'ct'})
    for pubtimelist in pubtimelists:
        pubtime = str(pubtimelist)
        print(pubtime)
        pubtimeResults = re.findall("04月[0-3][0-9]日", pubtime)#04月[0-3][0-9]日
        if len(pubtimeResults) !=0:
            li5.append(pubtimeResults[0])
        else:
            li5.append('null')
    print(li0)
    print(li1)
    print(li2)
    print(li3)
    print(li4)
    print(li5)

    for i in range(len(li0)):
        list_result = []
        if li5[i] !='null' and li1[i]!=':':
            list_result.append(li0[i])
            list_result.append(li1[i])
            list_result.append(li2[i])
            list_result.append(li3[i])
            list_result.append(li4[i])
            list_result.append(li5[i])
            print(list_result)
            list1_result.append(list_result)
        else:
            pass

def get_hot_search(url_base, page, keyword,list1_result):
    # search url need  urlencoe by twice
    params = {'keyword': keyword}
    res = parse.urlencode(params)
    url = url_base + res + "&page="+str(page)
    html=get_html(url)
    print(html)
    parse_html(html,list1_result)
def main():
    # create_db()
    url_base = "https://weibo.cn/search/mblog?hideSearchFrame=&"
    list1_result = []
    for page in range(50, 100):
        time.sleep(3)

        # keyword = '周扬青宣布与罗志祥分手'  #huati0
        # keyword = '周扬青宣布和罗志祥分手'  #huati0
        # keyword = '全国性哀悼活动举行'  # huati1
        # keyword = '山东高管性侵养女'  # huati2
        # keyword = '湖北武汉解封'  # huati3 一条4月份，其他6月份
        keyword = '2020年高考延期一个月举行'  # huati4  还没爬
        # keyword = '大学生拍摄虐猫视频贩卖'  # huati5
        # keyword = '天猫总裁蒋凡自请调查'  # huati6
        # keyword = '瑞幸咖啡财务造假事件'  # huati7
        # keyword = '交警扮盲人带导盲犬坐公交被赶'  # huati8
        # keyword = '“相信未来”线上义演'  # huati9 爬5月份
        get_hot_search(url_base, page, keyword,list1_result)
    sql = """INSERT INTO huati4(author,content,zan,zhuanfa,pinglun,public_time) VALUES (%s,%s,%s,%s,%s,%s)"""
    insert_db(sql,list1_result)

main()
