import time
def get_millisecond():
    """
    :return: 获取精确毫秒时间戳,13位
    """
    millis = int(round(time.time() * 1000))
    print(millis)
    millis = int(time.time())
    print(millis)

get_millisecond()