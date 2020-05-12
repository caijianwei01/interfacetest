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


if __name__ == '__main__':
    db = MysqlUtil('127.0.0.1', 3306, 'root', '123456', 'school')
    sql1 = "select USER_NAME, GUID from school_student where SCHOOL_ID='c42be09025eb851943bf77378b034d62' and AUTH_PIC_URL is not null limit 10;"
    rs1 = db.query(sql1)
    guids = []
    print(len(rs1))
    for rs in rs1:
        guids.append(rs[1])
    print(guids)
    guids_str = ','.join(guids)
    print(type(guids_str))
    # sql2 = 'insert into user values ("小明",17,"男")'
    # db.execute(sql2)
