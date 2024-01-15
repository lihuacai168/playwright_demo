# !/usr/bin/python3
# -*- coding: utf-8 -*-import pytest

import pytest
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

from pages.login_page import LoginPage

from log import logger

# @Author: 花菜
# @File: conftest.py
# @Time : 2024/1/13 00:42
# @Email: lihuacai168@gmail.com


def extract_domain(url_string):
    parsed_url = urlparse(url_string)
    return parsed_url.netloc

@pytest.fixture(scope="session")
def page(pytestconfig):
    with sync_playwright() as p:
        logger.info("page session fixture starting....")
        browser = p.chromium.launch(headless=True, timeout=5_000)
        context = browser.new_context()
        page = context.new_page()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        yield page
        logger.info("page session fixture closing.......")
        base_url = pytestconfig.getoption("base_url") or "http://119.91.147.215"
        domain = extract_domain(base_url).replace(".", "_")
        logger.info("stop tracing...")
        context.tracing.stop(path=f"{domain}_trace.zip")
        browser.close()


# 创建一个 pytest fixture 实现登录操作，并设置为session级别，实现共享登录状态
@pytest.fixture(scope="function")
def login(page, pytestconfig):
    default_url = "http://119.91.147.215"
    login_page = LoginPage(
        page, pytestconfig.getoption("base_url") or "http://119.91.147.215"
    )
    if login_page.base_url == default_url:
        logger.warning("使用默认登录地址，如果需要修改请使用命令行参数 --base-url")

    login_page.login("test", "test2020")
    yield login_page
    # 可以在这里添加断言确认登录成功


def pytest_addoption(parser):
    parser.addoption(
        "--host",
        action="store",
        default="http://119.91.147.215",
        help="base URL for login page",
    )
    logger.info("添加命令行参数 host")
    # parser.addoption("--base-url", action="store", default="http://119.91.147.215", help="base URL for login page")
