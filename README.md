
# 项目介绍 🚀
Pytest + Playwright + Allure UI自动化demo
目前有的功能：
- 🎯 UI自动化 Page Object 设计模式 
- 💻 Playwright 的基本使用（打开网页，元素定位，元素操作，网络等待，断言） 
- ⚙️ Pytest fixture 常见的使用方式
- 📝 Pytest 命令行各种常用的参数配置
- 📊 Allure 报告基本的装饰器使用
- 📋 Pytest + Allure 的log配置（自定义格式，控制台和 allure 报告隔离）
- 🚦 多环境并行测试（由 Github Action 实现）


# 项目结构 📚
```text
├── README.md                  # 📝 项目介绍及使用指南
├── allure-results             # 📊 Allure测试报告结果
├── log.py                     # 📁 日志配置文件
├── logs                       # 📂 存放日志的文件夹
│   ├── info.log               # 📎 日志文件
├── pages                      # 📑 页面类文件夹，按Page Object设计模式划分
│   └── login_page.py          # 🔐 登录页面自动化脚本
├── pytest.ini                 # ⚙️ pytest配置文件
├── requirements.txt           # 📃 存放项目依赖的Python库
├── testcases                  # 📁 测试用例文件夹
│   ├── conftest.py            # 🔧 存放pytest的fixture
│   ├── test_api_page.py       # 🌐 API测试用例
│   └── test_testcase_page.py  # 🧪 测试用例页面用例
└── trace.zip                  # 🔍 执行trace文件，定位分析错误非常有用
```
 

# 不要白嫖 🚫
**若你对我的项目感兴趣，或者对你有帮助，请⭐star和🍴fork，让我们共同完善和提升它。你的支持是我创新并持续改进的动力💪**

# 快速开始 ⏩
## 环境准备 🛠️
- Python 3.9+ 🐍
- Java 8+ (Allure依赖Java) ☕
- Allure [安装参考](https://github.com/allure-framework/allure2) 🎈

## 创建虚拟环境 🌐
```shell
python -m venv venv
```

## 安装依赖 📌
```shell
pip install -r requirements.txt
```

## 安装浏览器 🌐
```shell
playwright install
```

## 运行测试 🚀
```shell
pytest
```

## 生成测试报告 📊
```shell
allure serve allure-results
```