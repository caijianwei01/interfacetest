#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json


class RunMethod(object):
    """
    接口方法实现和封装
    """

    def post_main(self, url, data=None, json_data=None, **kwargs):
        """
        post请求
        :param url:
        :param data:
        :param json_data:
        :param kwargs:
        :return:
        """
        if data is not None:
            result = requests.post(url, data=data, verify=False, **kwargs)
        else:
            result = requests.post(url, json=json_data, verify=False, **kwargs)
        return result.json()

    def get_main(self, url, data=None, **kwargs):
        """
        get请求
        verify=False：表示忽略对SSL证书的验证
        :param url:
        :param data:
        :param headers:
        :return:返回结果为json格式
        """
        if data is not None:
            result = requests.get(url, params=data, verify=False, **kwargs)
        else:
            result = requests.get(url, verify=False, **kwargs)
        return result.json()

    def run_main(self, method, url, data=None, json_data=None, **kwargs):
        """
        调用封装方法
        ensure_ascii=False：不使用ascii编码
        :param method: "get"或者"post"请求
        :param url:
        :param data:
        :param json_data:
        :param kwargs:
        :return:
        """
        if str(method).lower() == "post":
            result = self.post_main(url, data=data, json_data=json_data, **kwargs)
        else:
            result = self.get_main(url, data=data, **kwargs)
        return json.dumps(result, ensure_ascii=False)
