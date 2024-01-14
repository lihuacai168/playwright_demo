# 使用指定的Playwright镜像作为基础镜像
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# 设定工作目录
WORKDIR /app

# 将本地代码复制到工作目录
COPY . /app

# 安装项目中需要的依赖
RUN pip install -r requirements.txt

# 给予pytest运行权限，并设为入口点
ENTRYPOINT ["pytest"]
