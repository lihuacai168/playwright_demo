# !/usr/bin/python3
# -*- coding: utf-8 -*-
import json
from urllib.parse import quote

import allure
from loguru import logger
from playwright.sync_api import expect

# @Author: 花菜
# @File: test_login.py
# @Time : 2024/1/13 00:16
# @Email: lihuacai168@gmail.com


# 测试
@allure.feature("测试登录成功")
@allure.step("login")
def test_项目列表(login):
    assert login.page.title() == "项目列表"
    expect(login.page.get_by_text("示例项目")).to_be_visible(timeout=3_000)


@allure.feature("API列表")
@allure.step("检查搜索API列表")
def test_api_list(login) -> None:
    logger.info("检查搜索API列表...")
    page = login.page

    login.switch2project_base()
    login.enter_project_detail()
    page.get_by_role("menuitem", name=" API 模板").click()
    expect(page.get_by_role("button", name="批量运行")).to_be_visible()
    expect(page.get_by_role("button", name="重置")).to_be_visible()
    expect(page.get_by_role("button", name="状态 ")).to_be_visible()

    search_api_name = "login"
    page.get_by_role("textbox", name="请输入接口名称").fill(search_api_name)
    # 定义你希望等待的接口地址
    get_api_path = (
        login.base_url
        + f"/api/fastrunner/api/?page=1&node=&project=7&search={quote(search_api_name)}&tag=&rigEnv=&onlyMe=true&showYAPI=true"
    )
    logger.info(f"等待接口地址：{get_api_path}")
    with page.expect_response(get_api_path) as response_info:
        data = json.loads(response_info.value.request.response().body().decode())
        logger.info(f"接口返回数据：{data}")
        expect(page.get_by_text(f"共 {data['count']} 条")).to_be_visible()
        logger.info("检查搜索API列表成功")


@allure.testcase("testcases/test_login.py")
@allure.feature("case列表")
@allure.step("case搜索")
def test_case_list(login) -> None:
    page = login.page
    logger.info("检查搜索case列表...")
    login.switch2project_base()
    login.enter_project_detail()

    page.get_by_role("menuitem", name=" 测试用例").click()
    search_testcase_name = "登录"
    page.get_by_placeholder("请输入用例名称").fill(search_testcase_name)
    get_test_case_path = f"/api/fastrunner/test/?project=7&node=&search={quote(search_testcase_name)}&searchType=1&caseType=&onlyMe=true&page=1"
    with page.expect_response(
        login.base_url + get_test_case_path, timeout=3000
    ) as case_response_info:
        data = json.loads(case_response_info.value.request.response().body().decode())
        logger.info(f"接口返回数据：{data}")
        expect(page.get_by_text(f"共 {data['count']} 条")).to_be_visible(timeout=3000)
        logger.info("检查搜索case列表成功")
