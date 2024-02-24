# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: log.py
# @Time : 2024/1/13 21:35
# @Email: lihuacai168@gmail.com

import logging
import os
import sys

from loguru import logger as uru_logger

BASEDIR = os.getcwd()


log_path = os.path.join(os.path.join(BASEDIR, "logs"), "info.log")
flag = 0
handler_id = 1
file_log_handler_flag = 0
allure_log_handler_flag = 0


class AllureHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)


class MyLogger:
    logger = uru_logger

    # log level: TRACE < DEBUG < INFO < SUCCESS < WARNING < ERROR < CRITICAL
    def __init__(self, level: str = "debug", log_file_path=log_path):
        self.stdout_handler(level="info")
        self.file_handler(level=level, log_file_path=log_file_path)
        # 多线程不开启allure日志，日志会被打乱
        self.allure_handler(level=level)

    def stdout_handler(self, level):
        """配置控制台输出日志"""
        global flag
        # 添加控制台输出的格式,sys.stdout为输出到屏幕;
        if flag != 0:
            return
            # 清空所有设置
        self.logger.remove()
        h_id = self.logger.add(
            sys.stdout,
            level=level.upper(),
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> "  # 颜色>时间
            "<m>[{thread.name}]</m>-"  # 进程名
            "<cyan>[{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
            ":<cyan>{line}]</cyan>-"  # 行号
            "<level>[{level}]</level>: "  # 等级
            "<level>{message}</level>",  # 日志内容
        )
        flag += 1
        global handler_id
        handler_id = h_id

    def file_handler(self, level, log_file_path):
        """配置日志文件"""
        global file_log_handler_flag
        # 控制只添加一个file_handler
        if file_log_handler_flag == 0:
            self.logger.add(
                log_file_path,
                level=level.upper(),
                format="{time:YYYY-MM-DD HH:mm:ss} "
                "[{thread.name}]-"
                "[{module}.{function}:{line}]-[{level}]:{message}",
                rotation="10 MB",
                encoding="utf-8",
            )
            file_log_handler_flag += 1

    def allure_handler(self, level):
        """日志输出到allure报告中"""
        _format = "{time:YYYY-MM-DD HH:mm:ss} [{module}.{function}:{line}]-[{level}]:{message}"
        self.logger.add(AllureHandler(), level=level.upper(), format=_format)

    @classmethod
    def change_level(cls, level):
        """更改stdout_handler级别"""
        # 清除stdout_handler配置
        logger.remove(handler_id=handler_id)
        # 重新载入配置
        cls.logger.add(
            sys.stdout,
            level=level.upper(),
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> "  # 颜色>时间
            "<m>[{process.name}]</m>-"  # 进程名
            "<m>[{thread.name}]</m>-"  # 进程名
            "<cyan>[{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
            ":<cyan>{line}]</cyan>-"  # 行号
            "<level>[{level}]</level>: "  # 等级
            "<level>{message}</level>",  # 日志内容
        )


_logger = MyLogger()
logger = _logger.logger
