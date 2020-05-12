#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json
import time
import hashlib
import util.mysql_util as mu


def get_pic():
    headers = {
        'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODc4ODE4NDIsImlhdCI6MTU4Nzc5NTQ0MiwiZGF0YSI6eyJ0b2tlbl9uYW1lIjoidXNlcl90b2tlbiIsImlkIjoyMCwidXNlcm5hbWUiOiJhaV9zY2hvb2wiLCJyb2xlIjoibm9ybWFsIn19.1p1m2qmGkgt_aGMaBfvzine85LQ1UlZpTxiLeHag6JI'}
    for i in range(59, 451):
        print(f'第{i}页')
        url = f'http://attendance.yooticloud.cn/api/v1/provider/user?pageNo={i}&pageSize=30&source=web'
        r = requests.get(url, headers=headers)
        for person in r.json()['data']:
            pic_url = person['url']
            if pic_url:
                try:
                    r1 = requests.get(pic_url[0])
                    with open('C:/Users/admin/Desktop/云校学生照片/%s.jpg' % person['name'], 'wb') as f:
                        f.write(r1.content)
                except Exception as e:
                    print(f'{person["name"]}学生图片路径异常')
                    print(e)
            else:
                print(f'{person["name"]}学生图片路径为空')
        print(f'第{i}页下载结束')


def calc_sign():
    """
    获取md5加密签名
    :return:
    """
    timestamp = str(int(time.time()))
    app_secret, app_key = "47F9B660196F0F23B55908786E8A327B", "E1B559D014E90F7EF8047949A7440F3E"
    md5_val = hashlib.md5((app_key + str(timestamp) + app_secret).lower().encode('utf-8')).hexdigest()
    return md5_val


def app_auth():
    """
    获取设备销权token
    :return:
    """
    url = 'http://attendance.yooticloud.cn/api/v1/app/auth'
    data = {
        'app_id': '15676497800668552d',
        'app_key': 'E1B559D014E90F7EF8047949A7440F3E',
        'timestamp': str(int(time.time())),
        'sign': calc_sign()
    }
    rs = requests.post(url, data=json.dumps(data))
    return rs.json()['data']


def auth_person(seq_no, guids, headers=None):
    """
    设备授权人员
    :param seq_no:
    :param guids:
    :return: {'code': 1, 'data': None, 'msg': True},code=1授权成功
    """
    url = 'http://attendance.yooticloud.cn/api/v1/provider/device/auth_person'
    payload = {
        "seq_no": seq_no,
        "guids": guids
    }
    rs = requests.post(url, data=json.dumps(payload), headers=headers)
    return json.loads(rs.text)


def cancle_auth_person(seq_no, guids, token):
    """
    :param seq_no: 设备序列号
    :param guids: 人员编号
    :param token:销权token
    :return:{'code': 1, 'data': None, 'msg': True}，code=1销权成功
    """
    url = 'http://attendance.yooticloud.cn/api/v1/provider/device/cancel_auth_person'
    headers = {
        'token': token
    }
    data = {
        'seq_no': seq_no,
        'guids': guids
    }
    rs = requests.post(url, data=json.dumps(data), headers=headers)
    return json.loads(rs.text)


def many_person_empower(myurl, headers):
    for i in range(1, 2):
        url1 = f'http://attendance.yooticloud.cn/api/v1/provider/user?pageNo={i}&pageSize=30&source=web'
        r = requests.get(url1, headers=headers)
        for person in r.json()['data']:
            pic_url = person['url']
            guid = person['guid']
            guid_len = len(guid)
            if pic_url:
                try:
                    code = auth_person(myurl, headers, guid)
                    if code == 1:
                        print(f"{person['name']}授权成功:{guid}-{guid_len}")
                    else:
                        print(f"{person['name']}授权失败:{guid}-{guid_len}")
                    time.sleep(1)
                except Exception as e:
                    print(f'{person["name"]}学生图片路径异常')
                    print(e)


if __name__ == '__main__':
    db = mu.MysqlUtil('127.0.0.1', 3306, 'root', '123456', 'school')
    sql1 = "select USER_NAME, GUID from school_student where SCHOOL_ID='c42be09025eb851943bf77378b034d62' and AUTH_PIC_URL is not null limit 10;"
    rs1 = db.query(sql1)
    guids = []
    for rs in rs1:
        guids.append(rs[1])
    guids_str = ','.join(guids)
    print(guids_str)
    seq_no = '5L03R090145'
    guids_1 = guids_str
    headers = {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODkzMzUwMTUsImlhdCI6MTU4OTI0ODYxNSwiZGF0YSI6eyJ0b2tlbl9uYW1lIjoiYXBwX3Rva2VuIiwiaWQiOjUsInVzZXJuYW1lIjoiYXBwX2lkIiwicm9sZSI6IiJ9fQ.B2WnsHkMsp9hNTw19mqS66EkQ-pwUsvJS4TSq1vSNLQ"
    }
    r1 = auth_person(seq_no, guids_1, headers)
    print(r1)
