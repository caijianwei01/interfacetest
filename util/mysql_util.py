#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql


class MysqlUtil:
    """mysql连接数据库操作"""

    def __init__(self, host, port, user, passwd, db):
        self.conn = pymysql.connect(host=host,
                                    port=port,
                                    user=user,
                                    passwd=passwd,
                                    db=db)
        self.cur = self.conn.cursor()

    def __del__(self):
        """
        析构函数，实例删除时触发。关闭游标和数据库连接
        """
        self.cur.close()
        self.conn.close()

    def query(self, sql):
        """
        查询数据
        :param sql: 查询sql
        :return:返回所有查询数据
        """
        self.cur.execute(sql)
        return self.cur.fetchall()

    def execute(self, sql):
        """
        执行sql语句
        :param sql:
        :return:
        """
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)
