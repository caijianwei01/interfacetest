#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
考勤平台常量
"""
URL = "http://attendance.yooticloud.yt/api/v1/"
# URL = "http://192.168.0.92:8080/"

# 设备授权人员
AUTH_PERSON = URL + "provider/device/auth_person"
# 设备销权人员
CANCEL_AUTH_PERSON = URL + "provider/device/cancel_auth_person"
# 远程开门
DEVICE_INTERACTIVE = URL + "provider/device/device_interactive"
# APP鉴权
AUTH = URL + "app/auth"
# 根据guid获取人员姓名和图片地址
QUERY_USER_INFO = URL + "provider/user/query_user_info"
