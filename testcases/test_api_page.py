# !/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import uuid
from urllib.parse import quote

import allure
from playwright.sync_api import Page, expect

from log import logger


# @Author: 花菜
# @File: test_api_page.py
# @Time : 2024/1/13 17:14
# @Email: lihuacai168@gmail.com
@allure.feature("API列表")
@allure.step("检查搜索API列表")
def test_api_list(login_and_goto_project_detail, page) -> None:
    logger.info("检查搜索API列表...")
    page.get_by_role("menuitem", name=" API 模板").click()
    expect(page.get_by_role("button", name="批量运行")).to_be_visible()
    expect(page.get_by_role("button", name="重置")).to_be_visible()
    expect(page.get_by_role("button", name="状态 ")).to_be_visible()

    search_api_name = "login"
    page.get_by_role("textbox", name="请输入接口名称").fill(search_api_name)
    # 定义你希望等待的接口地址
    get_api_path = (
        login_and_goto_project_detail.base_url
        + f"/api/fastrunner/api/?page=1&node=&project=7&search={quote(search_api_name)}&tag=&rigEnv=&onlyMe=true&showYAPI=true"
    )
    logger.info(f"等待接口地址：{get_api_path}")
    with page.expect_response(get_api_path) as response_info:
        data = json.loads(response_info.value.request.response().body().decode())
        logger.info(f"接口返回数据：{data}")
        expect(page.get_by_text(f"共 {data['count']} 条")).to_be_visible()
        logger.info("检查搜索API列表成功")


@allure.feature("API列表")
@allure.step("增加然后删除API")
def test_api_add_del(login_and_goto_project_detail: Page, page: Page) -> None:
    page.get_by_role("menuitem", name=" API 模板").click()
    logger.info("点击测试分组")
    page.get_by_text(" 测试分组").click()
    page.get_by_role("button", name=" 添加接口").click()
    page.get_by_role("textbox", name="请输入接口名称").click()
    page.get_by_role("textbox", name="请输入接口名称").fill("ui")
    page.get_by_role("textbox", name="请输入接口名称").press("Enter")
    api_name = "ui自动化添加" + uuid.uuid4().hex
    page.get_by_role("textbox", name="请输入接口名称").fill(api_name)
    page.get_by_placeholder("请输入接口请求地址").click()
    page.get_by_placeholder("请输入接口请求地址").fill("/hello")
    page.get_by_role("button", name="Save", exact=True).click()
    logger.info("点击保存按钮")
    expect(page.get_by_text(f"POST /hello {api_name}").first).to_be_visible(
        timeout=1_000
    )
    logger.info("断言添加接口成功")

    # 删除接口
    logger.info("删除接口")
    page.get_by_text(f"POST /hello {api_name}").first.click()
    page.get_by_role("cell", name="   ").get_by_role("button").nth(3).click()
    page.get_by_role("button", name="").click()
    page.get_by_role("button", name="确定").click()
    logger.info("点击确定按钮")
    expect(page.get_by_text(f"POST /hello {api_name}").first).not_to_be_visible(
        timeout=1_000
    )
    logger.info("断言删除接口成功")
