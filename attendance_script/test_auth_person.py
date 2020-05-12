#!/usr/bin/env python
# -*- coding:utf-8 -*-
import unittest
import common.atten_const as const
import common.runmethod as run
import json


class TestAuthPerson(unittest.TestCase):
    def setUp(self):
        self.run_method = run.RunMethod()
        self.data = {
            "seq_no": "5L03R090145",
            "guid": "1589256263348"
        }
        self.headers = {
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODkzMzUwMTUsImlhdCI6MTU4OTI0ODYxNSwiZGF0YSI6eyJ0b2tlbl9uYW1lIjoiYXBwX3Rva2VuIiwiaWQiOjUsInVzZXJuYW1lIjoiYXBwX2lkIiwicm9sZSI6IiJ9fQ.B2WnsHkMsp9hNTw19mqS66EkQ-pwUsvJS4TSq1vSNLQ"
        }

    def tearDown(self):
        pass

    def test_auth_person_success(self):
        rs = self.run_method.run_main("post", const.AUTH_PERSON, json_data=self.data, headers=self.headers)
        self.assertEqual(1, json.loads(rs)['code'], "设备授权人员失败")


if __name__ == '__main__':
    unittest.main()
