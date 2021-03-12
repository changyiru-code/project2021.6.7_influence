# 访问测试报告
from flask import Flask

app = Flask(__name__)
@app.route('/report_ikang', methods=['get'])
def index():
    page = open(file_ikang, encoding='utf-8')
    res = page.read()
    return res

@app.route('/report_tjb', methods=['get'])
def index_1():
    page = open(file_tjb, encoding='utf-8')
    res = page.read()
    return res


app.run(host='0.0.0.0', port=12345)