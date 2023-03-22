# promalert-feishu-webhook

python3.11 + flask 编写了一个对接飞书 API 实现告警的 webhook

## 飞书机器人概述

```shell
https://www.feishu.cn/hc/zh-CN/articles/244506653275#tabs0|lineguid-AHuiGI
```

## 安全设置

### 签名校验

```shell
https://www.feishu.cn/hc/zh-CN/articles/244506653275
```

## 构建镜像

```shell
DATE=$(date +'%Y%m%d')
TIMESTAMP=$(date +%s)
docker build -t promalert-feishu-webhook:${DATE}-v${TIMESTAMP} .
sed -i "s@TAG@${DATE}-v${TIMESTAMP}@g" docker-compose.yml
```

## 启动服务

1. 更改 docker-compose.yml 中的镜像
2. 设置`APP_FS_WEBHOOK`环境变量为你自己的飞书的`webhook`地址
3. 设置`APP_FS_SECRET`环境变量为你自己的飞书群机器人的签名校验秘钥
4. 启动服务

```shell
docker-compose up -d
```
