#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# *******************************************
# -*- CreateTime  :  2023/03/15 13:14:36
# -*- Author      :  Allen_Jol
# -*- FileName    :  config.py
# -*- Desc        :  None
# *******************************************

import os
import sys
"""
这是一个项目使用的配置文件.

飞书的 webhook 地址默认为 None,其他的配置文件如果环境变量不设置,那都会在这个配置文件中设置一个默认值(缺省值)

即: 
    APP_ENV 和 APP_FS_WEBHOOK 是两个必填的环境变量
"""

# 默认是 dev 环境，会开启 DEBUG 模式.如果 docker-compose.yml 中设置 APP_ENV: prod，则关闭 DEBUG 模式
if os.getenv("APP_ENV") == "dev":
    DEBUG = True
elif os.getenv("APP_ENV") == "prod":
    DEBUG = False
else:
    print("Environment APP_ENV value false, please set to dev or prod!")
    sys.exit(1)

# 项目侦听的地址
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")

# 项目使用的端口
APP_PORT = os.getenv("APP_PORT", "8080")

# 必须在 docker-compose.yml 中设置飞书的 webhook 地址. 
# 默认该 webhook 地址为空,为空则无法正常启动该 webhook 服务
APP_FS_WEBHOOK = os.getenv("APP_FS_WEBHOOK", None)

# 必须在 docker-compose.yml 中设置飞书自定义机器人安全设置中的签名校验秘钥.
# 默认该 签名校验秘钥为空,为空则无法正常启动该 webhook 服务
APP_FS_SECRET = os.getenv("APP_FS_SECRET", None)
