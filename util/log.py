#!/usr/bin/env python
# -*- coding:utf-8 -*-
import util.util_const as ut
import logging
import logging.config


class Log(object):
    def __init__(self):
        # 读取日志配置文件
        log_cnf = ut.PARENT_DIR_PATH + '\\config\\Logger.conf'
        logging.config.fileConfig(log_cnf)
        print(log_cnf)
        # 选择一个日志格式
        self.logger = logging.getLogger('example02')

    def debug(self, message):
        """定义debug级别日志打印方法"""
        self.logger.debug(message)

    def info(self, message):
        """定义info级别日志打印方法"""
        self.logger.info(message)

    def warning(self, message):
        """定义waring级别日志打印方法"""
        self.logger.warning(message)

    def error(self, message):
        """定义error级别日志打印方法"""
        self.logger.error(message)


if __name__ == '__main__':
    my_log = Log()
    my_log.debug('debug日志测试')
    my_log.info('info日志测试')
    my_log.warning('waring日志测试')
    my_log.error('error日志测试')
