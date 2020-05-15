#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""常用工具类"""

import random
import os
import time
from datetime import datetime
from PIL import Image
from datetime import date
from datetime import timedelta
import util.util_const as ut


def create_phone(phone_nums=1):
    """
    自动生成手机号，默认返回一个手机号，多个以列表的形式返回
    :param phone_nums: 生成手机号数
    :return:
    """
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


def _getdistrictcode():
    """
    读取区号文件数据
    :return:
    """
    code_list = []
    with open('../data/districtcode.txt', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        # 获取辖区的区号
        if line.strip() and line[:6][-2:] != '00':
            code_list.append(line[:6])
    return code_list


def create_id_card(card_nums=1):
    """
    自动生成身份证，默认返回一个身份证，多个以列表的形式返回
    :param card_nums: 生成身份证数
    :return:
    """
    id_cards = []
    for num in range(int(card_nums)):
        code_list = _getdistrictcode()
        id_card = code_list[random.randint(0, len(code_list) - 1)]  # 地区项
        id_card = id_card + str(random.randint(1950, 2000))  # 年份项
        day = date.today() + timedelta(days=random.randint(1, 366))  # 月份和日期项
        id_card = id_card + day.strftime('%m%d')
        id_card = id_card + str(random.randint(100, 300))  # 顺序号简单处理
        count = 0
        weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
        check_code = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5',
                      '9': '3',
                      '10': '2'}  # 校验码映射
        for i in range(0, len(id_card)):
            count = count + int(id_card[i]) * weight[i]
        id_card = id_card + check_code[str(count % 11)]  # 算出校验码
        if int(card_nums) == 1:
            return id_card
        id_cards.append(id_card)
    return id_cards


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


def get_current_datetime(get_date=True, get_time=True, date_separator='-', time_separator=':', datetime_separator=' '):
    """
    获取当前的日期时间
    :param get_date: 是否获取日期
    :param get_time: 是否获取时间
    :param date_separator: 日期分隔符，默认'-'
    :param time_separator: 时间分隔符，默认':'
    :return:
    """
    current_date = ''
    now_time = ''
    # 获取日期
    if get_date:
        time_tup = time.localtime()
        current_date = str(time_tup.tm_year) + f'{date_separator}' + str(time_tup.tm_mon) + f'{date_separator}' + str(
            time_tup.tm_mday)
    # 获取时间
    if get_time:
        date_time = datetime.now()
        now_time = date_time.strftime(f'%H{time_separator}%M{time_separator}%S')
    if get_date and get_time:
        return current_date + datetime_separator + now_time
    elif get_date:
        return current_date
    elif get_time:
        return now_time


if __name__ == '__main__':
    reduct_image_by_width(width=480)
