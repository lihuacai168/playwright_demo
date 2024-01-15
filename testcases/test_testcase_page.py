# !/usr/bin/python3
# -*- coding: utf-8 -*-
import json
from urllib.parse import quote

import allure
from playwright.sync_api import expect

from log import logger


# @Author: 花菜
# @File: test_testcase_page.py
# @Time : 2024/1/13 17:14
# @Email: lihuacai168@gmail.com
@allure.testcase("testcases/test_login.py")
@allure.feature("case列表")
@allure.step("case搜索")
def test_case_list(login_and_goto_project_detail, page) -> None:
    logger.info("检查搜索case列表...")
    page.get_by_role("menuitem", name=" 测试用例").click()
    search_testcase_name = "登录"
    page.get_by_placeholder("请输入用例名称").fill(search_testcase_name)
    get_test_case_path = f"/api/fastrunner/test/?project=7&node=&search={quote(search_testcase_name)}&searchType=1&caseType=&onlyMe=true&page=1"
    logger.info(f"等待接口地址：{get_test_case_path}")
    with page.expect_response(
        login_and_goto_project_detail.base_url + get_test_case_path, timeout=3000
    ) as case_response_info:
        data = json.loads(case_response_info.value.request.response().body().decode())
        logger.info(f"接口返回数据：{data}")
        expect(page.get_by_text(f"共 {data['count']} 条")).to_be_visible(timeout=3000)
        logger.info("检查搜索case列表成功")
