# !/usr/bin/python3
# -*- coding: utf-8 -*-import pytest
import pytest
from playwright.sync_api import sync_playwright
from loguru import logger

from pages.login_page import LoginPage


# @Author: 花菜
# @File: conftest.py
# @Time : 2024/1/13 00:42
# @Email: lihuacai168@gmail.com


# 创建一个 pytest fixture 实现浏览器的初始化和结束操作
# @pytest.fixture(scope="session")
# def page():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#         yield page
#         browser.close()


# 创建一个 pytest fixture 实现浏览器的初始化和结束操作
@pytest.fixture(scope="session")
def page():
    with sync_playwright() as p:
        logger.info("starting....")
        browser = p.chromium.launch(headless=True, timeout=5000)
        context = browser.new_context()
        page = context.new_page()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        yield page
        logger.info("closing.......")
        context.tracing.stop(path="trace.zip")
        browser.close()


# 创建一个 pytest fixture 实现登录操作，并设置为session级别，实现共享登录状态
@pytest.fixture(scope="session")
def login(page):
    login_page = LoginPage(page)
    login_page.login("test", "test2020")
    yield login_page
    # 可以在这里添加断言确认登录成功
