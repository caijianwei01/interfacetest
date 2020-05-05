#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json


class RunMethod(object):
    """
    接口方法实现和封装
    """

    def post_main(self, url, data, headers=None):
        if headers is not None:
            result = requests.post(url=url, data=data, headers=headers)
        else:
            result = requests.post(url=url, data=data)
        return result.json()

    def get_main(self, url, data=None, headers=None):
        """
        verify=false：表示忽略对SSL证书的验证
        ensure_ascii=False：中文默认不使用不使用ascii编码
        :param url:
        :param data:
        :param headers:
        :return:返回结果为json格式
        """
        if headers is not None:
            result = requests.get(url=url, data=data, headers=headers, verify=False)
        else:
            result = requests.get(url=url, data=data, verify=False)
        return result.json()

    def run_main(self, method, url, data=None, headers=None):
        if str(method).lower() == "post":
            result = self.post_main(url, data, headers=headers)
        else:
            result = self.get_main(url, data=data, headers=headers)
        return json.dumps(result, ensure_ascii=False)
