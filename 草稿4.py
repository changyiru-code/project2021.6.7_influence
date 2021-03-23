##2每次测试正确代码都用这个
import requests, json

headers = {'Content-Type': 'text/html;charset=UTF-8'}
data = {
    'eventNoticeType': 'SOCIAL_INFLUENCE',
    'eventState': 'SUCCESSFUL',
    'topicId': 'ff557982-43d8-4256-a256-0d0854ef114a',
}
# url = 'http://10.20.2.181:8088/notice'  # http://10.20.2.181:8088/notice
url = 'http://127.0.0.1:8088/notice'
r = requests.post(url, data=data)
print(r.text)
print(r.url)
