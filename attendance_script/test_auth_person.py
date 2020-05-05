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
            "seq_no": "SN1376838",
            "guid": "ec368c226c98b42fef1e47cef3d89714"
        }

    def tearDown(self):
        pass

    def test_auth_person_success(self):
        rs = self.run_method.run_main("post", const.AUTH_PERSON, json_data=self.data)
        self.assertEqual(1, json.loads(rs)['code'], "设备授权人员失败")


if __name__ == '__main__':
    unittest.main()
