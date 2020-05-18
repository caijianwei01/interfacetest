#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib
import json
import time
import requests
import common.atten_const as at
import util.mysql_util as mu
from util.log import Log

# 日志打印
my_log = Log()


def get_person_pic():
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
    url = at.AUTH
    data = {
        'app_id': '15676497800668552d',
        'app_key': 'E1B559D014E90F7EF8047949A7440F3E',
        'timestamp': str(int(time.time())),
        'sign': calc_sign()
    }
    rs = requests.post(url, data=json.dumps(data))
    return rs.json()['data']


def auth_person(seq_no, guids, token):
    """
    设备授权人员
    :param seq_no:
    :param guids:
    :return: {'code': 1, 'data': None, 'msg': True},code=1授权成功
    """
    url = at.AUTH_PERSON
    payload = {
        "seq_no": seq_no,
        "guids": guids
    }
    start = time.time()
    rs = requests.post(url, data=json.dumps(payload), headers={'token': token}, timeout=(10, 3600))
    end = time.time()
    times = (end - start) / 60
    times = round(times, 2)
    my_log.info(f"{seq_no}耗费时间{times}分钟")
    try:
        return rs.json()
    except Exception as e:
        return {"code": -1, "msg": str(e), "data1": "", "data": ""}


def auths_persons(seq_no, token, school_id, limit=None):
    """
    一台设备批量授权人员
    :param seq_nos:
    :param guids:
    :param token:
    :param school_id:
    :param limit:
    :return:
    """
    # 数据库连接
    db = mu.MysqlUtil('127.0.0.1', 3306, 'root', '123456', 'school')
    # 获取学校人员guids
    if limit:
        sql = "select USER_NAME, GUID from school_student " \
              "where SCHOOL_ID='{}' and AUTH_PIC_URL is not null limit {};".format(str(school_id), int(limit))
    else:
        sql = f"select USER_NAME, GUID from school_student " \
              "where SCHOOL_ID='{}' and AUTH_PIC_URL is not null;".format(str(school_id))
    persons = db.query(sql)
    guids = []
    for person in persons:
        guids.append(person[1])
    guids_str = ','.join(guids)
    my_log.info(f'{seq_no}开始授权，授权人数{len(guids)}...')
    result = auth_person(seq_no, guids_str, token)
    if isinstance(result, dict):
        if result.get('data1'):
            my_log.info(f"{seq_no} --> 授权失败人员：")
            for rs in result.get('data1'):
                if rs:
                    my_log.info(rs.get('msg'))
                    my_log.info('------------------------------------------------')


def query_user_info():
    persons = []
    with open('../data/刘美小学.txt') as f:
        guids = f.readlines()
    for guid in guids:
        rs = requests.get(at.QUERY_USER_INFO, params={'guid': guid.strip()})
        persons.append(rs.json().get('data'))
    for p in persons:
        if p:
            url = p.get('url')
            if url:
                try:
                    rs = requests.get(url)
                    with open('C:/Users/admin/Desktop/刘美异常照片/%s.jpg' % p.get('name'), 'wb') as f:
                        f.write(rs.content)
                except Exception as e:
                    my_log.info(f"{p.get('name')}图片路径异常：{e}")
            else:
                my_log.info(f"{p.get('name')}--{p.get('guid')}:图片路径为空")
        else:
            my_log.info(f"查询学生guid失败-->{p}")


def cancle_auth_person(seq_no, guids, token):
    """
    :param seq_no: 设备序列号
    :param guids: 人员编号
    :param token:销权token
    :return:{'code': 1, 'data': None, 'msg': True}，code=1销权成功
    """
    url = at.CANCEL_AUTH_PERSON
    headers = {
        'token': token
    }
    data = {
        'seq_no': seq_no,
        'guids': guids
    }
    rs = requests.post(url, data=json.dumps(data), headers=headers)
    return json.loads(rs.text)


if __name__ == '__main__':
    from multiprocessing.pool import ThreadPool

    seq_list = ['5C04R080066', '5C04R080068', '5C04R080024']
    pool = ThreadPool(len(seq_list))
    token = app_auth()
    school_id = '4c59e358765ca0828cc994b7b5992313'
    for seq in seq_list:
        pool.apply_async(auths_persons, args=(seq, token, school_id))
        time.sleep(30)
    pool.close()
    pool.join()
