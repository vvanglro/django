import json

import requests


def send_get(url, data, header):
    res = requests.get(url=url, params=json.dumps(data), headers=header)
    res = json.loads(res.text)
    return res


def send_post(url, data, header):
    res = requests.post(url=url, data=data, headers=header)
    res = res.text
    return res


def run_main(url, method, data=None, header=None):
    res = None
    if method == 'GET':
        res = send_get(url, data, header)
    else:
        res = send_post(url, data, header)
    return res

if __name__ == '__main__':
    url = 'http://localhost:8088/woniusales/user/login'
    method = 'post'
    data = {'username': 'admin','password': 'admin123','verifycode': '0000'}
    print(type(data))
    header ={ 'Content - Type': 'application / x - www - form - urlencoded;charset = UTF - 8'}
    print(type(header))
    re = run_main(url,method, data=data, header=header)
    print(re)