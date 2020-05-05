#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import json
import hashlib
import common.atten_const as const
import common.runmethod as rd


class AttendanceUtil(object):
    def __init__(self):
        self.run_method = rd.RunMethod()

    def calc_sign(self):
        """
        获取md5加密签名
        :return:
        """
        timestamp = str(int(time.time()))
        app_secret, app_key = "47F9B660196F0F23B55908786E8A327B", "E1B559D014E90F7EF8047949A7440F3E"
        md5_val = hashlib.md5((app_key + str(timestamp) + app_secret).lower().encode('utf-8')).hexdigest()
        return md5_val

    def app_auth(self):
        """
        获取设备销权token
        :return:
        """
        data = {
            'app_id': '15676497800668552d',
            'app_key': 'E1B559D014E90F7EF8047949A7440F3E',
            'timestamp': str(int(time.time())),
            'sign': self.calc_sign()
        }
        # rs = requests.post(const.AUTH, data=json.dumps(data))
        rs = self.run_method.run_main("post", const.AUTH, json.dumps(data))
        print(rs)


if __name__ == '__main__':
    att_util = AttendanceUtil()
    print(att_util.app_auth())
