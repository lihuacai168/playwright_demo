# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: login_page.py.py
# @Time : 2024/1/13 00:16
# @Email: lihuacai168@gmail.com

from playwright.sync_api import Page
import allure
from log import logger


class LoginPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    # 定义页面元素
    def username_input(self):
        return self.page.locator("#email")

    def password_input(self):
        return self.page.locator("#pwd")

    def submit_button(self):
        return self.page.locator("#submitBtn")

    # 定义操作
    @allure.step("打开登录页面，填写账号密码")
    def login(self, username: str, password: str):
        logger.info(f"打开登录页面: {self.base_url + '/fastrunner/login'}，填写账号密码")
        self.page.goto(self.base_url + "/fastrunner/login")
        self.username_input().fill(username)
        self.password_input().fill(password)
        logger.info("点击登录按钮")
        self.submit_button().click()
        self.page.wait_for_load_state("networkidle", timeout=3_000)
        logger.info("登录成功")

    @allure.step("切换项目列表首页")
    def switch2project_base(self, project_id=7):
        logger.info("切换项目列表首页")
        self.page.goto(
            self.base_url + f"/fastrunner/api_record/{project_id}", timeout=3000
        )
        self.page.get_by_role("menuitem", name=" 首 页").click()

    @allure.step("从项目列表进入项目详情")
    def enter_project_detail(self, project_name="示例项目"):
        logger.info(f"从项目列表进入项目详情：{project_name=}")
        self.page.get_by_text(project_name, exact=True).click()

    @allure.step("登录并进入项目详情")
    def login_and_to_project_detail(self, username, password, project_name):
        self.login(username, password)
        self.switch2project_base()
        self.enter_project_detail(project_name)