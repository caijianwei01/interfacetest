#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""常用工具类"""

import random
import os
from PIL import Image
import util.util_const as ut


def create_phone(phone_nums=1):
    """
    自动生成手机号，默认返回一个手机号，多个以列表的形式返回
    :param phone_nums: 生成手机号数
    :return:
    """
    if int(phone_nums) != 1:
        phones = []
    for i in range(int(phone_nums)):
        # 第二位数字
        second = [3, 4, 5, 7, 8][random.randint(0, 4)]
        # 第三位数字
        third = {
            3: random.randint(0, 9),
            4: [5, 7, 9][random.randint(0, 2)],
            5: [i for i in range(10) if i != 4][random.randint(0, 8)],
            7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
            8: random.randint(0, 9)}[second]
        # 最后八位数字
        suffix = random.randint(9999999, 100000000)
        # 拼接手机号，单个返回
        if phone_nums == 1:
            return f"1{second}{third}{suffix}"
        phones.append(f"1{second}{third}{suffix}")
    return phones


def create_name(name_nums=1):
    """
    自动生成姓名，默认返回一个姓名，多个姓名以列表的形式返回
    :param name_nums: 生成姓名数
    :return:
    """
    names = []
    for i in range(int(name_nums)):
        x = random.randint(0, len(ut.SURNAME) - 1)
        m1 = random.randint(0, len(ut.NAME) - 1)
        m2 = random.randint(0, len(ut.NAME) - 1)
        # 名个个数
        name_num = random.choice([1, 2])
        # 返回单个姓名
        if name_nums == 1:
            if name_num == 1:
                return f"{ut.SURNAME[x]}{ut.NAME[m1]}"
            elif name_num == 2:
                return f"{ut.SURNAME[x]}{ut.NAME[m1]}{ut.NAME[m2]}"
        # 多个姓名加入列表
        if name_num == 1:
            names.append(f"{ut.SURNAME[x]}{ut.NAME[m1]}")
        elif name_num == 2:
            names.append(f"{ut.SURNAME[x]}{ut.NAME[m1]}{ut.NAME[m2]}")
    return names


def reduct_image_by_width(width: int = 600, img_path: str = "../img/"):
    """
    图片压缩
    :param width:
    :param img_path:
    :return:
    """
    all_image = os.listdir(img_path)
    for image in all_image:
        file = img_path + image
        img = Image.open(file)
        w, h = img.size
        new_height = round(width / w * h)
        img = img.resize((width, new_height), Image.ANTIALIAS)
        if "." in image:
            filename = image.split(".")[0]
        else:
            filename = image
        filename = filename + "_update" + ".jpg"
        img.save(img_path + filename, optimize=True, quality=95)


if __name__ == '__main__':
    print(create_name(100))
