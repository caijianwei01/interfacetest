#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
考勤平台常量
"""
URL = "http://attendance.yooticloud.cn/"

# 设备授权人员
AUTH_PERSON = URL + "api/v1/provider/device/auth_person"
# 设备销权人员
CANCEL_AUTH_PERSON = URL + "api/v1/provider/device/cancel_auth_person"
# 远程开门
DEVICE_INTERACTIVE = URL + "api/v1/provider/device/device_interactive"
# APP鉴权
AUTH = URL + "api/v1/app/auth"
