# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: test_fast_po.py
# @Time : 2024/1/12 23:31
# @Email: lihuacai168@gmail.com


import allure
import pytest
import unittest
import logging
from allure_commons.types import AttachmentType
from playwright.sync_api import sync_playwright, Page
from playwright.sync_api import expect
from loguru import logger


class LoginPage:
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.screenshot_counter = 1
        self.base_url = 'http://119.91.147.215'

    @pytest.fixture(scope="class", autouse=True)
    def run_after_every_method(self):
        logger.info("run_after_every_method...")
        # 在这里面你可以放置一些在方法执行前要进行的设置程序
        # ...
        yield
        # yield 语句后面的代码将在测试方法执行完之后运行
        print("A method has just finished!")
        self.tearDown()

    def tearDown(self):
        self.take_screenshot_and_attach()

    def take_screenshot_and_attach(self):
        screenshot_name = f"screenshot_{self.screenshot_counter}"
        screenshot_path = f"{screenshot_name}.png"
        self.page.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, attachment_type=AttachmentType.PNG)
        self.screenshot_counter += 1

    @allure.step("打开登录页面")
    def open_login_page(self):
        self.page.goto(self.base_url + "/fastrunner/login")
        # self.take_screenshot_and_attach()

    @allure.step("打开登录页面")
    def open_project_info(self):
        self.page.goto(self.base_url + "/fastrunner/project/7/dashbord")
        # self.take_screenshot_and_attach()
    @allure.step("输入账号密码")
    def input_username_password(self, username, password):
        self.page.fill('#email', username)
        self.page.fill('#pwd', password)
        # self.take_screenshot_and_attach()

    @allure.step("点击登录")
    def click_login_button(self):
        self.page.click('#submitBtn')
        self.page.wait_for_load_state("networkidle")
        # self.take_screenshot_and_attach()

    @allure.step("断言页面上是否有“项目看板”这个文字")
    def assert_project_board_text(self):
        assert "项目看板" in self.page.content()


@pytest.fixture(scope="session")
def playwright():
    return sync_playwright().start()


@pytest.fixture(scope="function")
def context(playwright):
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(context):
    logger.info("new page...")
    p = context.new_page()
    yield p
    logger.info("take a shot...")
    p.screenshot()
    p.close()


@allure.feature("登录功能")
@allure.story("登录成功")
@allure.severity(allure.severity_level.CRITICAL)
def test_login(page):
    login_page = LoginPage(page)
    login_page.open_login_page()
    login_page.input_username_password('test', 'test2020')
    login_page.click_login_button()
    login_page.assert_project_board_text()



@allure.feature("健康拨测模块")
@allure.story("测试健康拨测模块")
class Test_HealthCheck:

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page
        yield
        logger.info("clos...")
        # self.page.close()

    @pytest.mark.run(order=0)
    def test_login_page(self, page: Page):
        login_page = LoginPage(page)
        login_page.open_login_page()
        login_page.input_username_password('test', 'test2020')
        login_page.click_login_button()
        login_page.assert_project_board_text()


    @pytest.mark.run(order=2)
    def test_login_pwd(self):
        login_page = LoginPage(self.page)
        login_page.open_project_info()
        expect(login_page.page.get_by_text("示例项目")).to_be_visible(timeout=3_000)

