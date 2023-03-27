# promalert-feishu-webhook

python3.11 + flask 编写了一个对接飞书 API 实现告警的 webhook

## 飞书机器人概述

```shell
https://www.feishu.cn/hc/zh-CN/articles/244506653275#tabs0|lineguid-AHuiGI
```

## 飞书开发文档

```shell
https://open.feishu.cn/document/ukTMukTMukTM/uADOwUjLwgDM14CM4ATN
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
cat docker-compose.yml | egrep [0-9]{8}\-v[0-9]{10} -o | xargs -i sed -i s#{}#${DATE}-v${TIMESTAMP}#g docker-compose.yml
```

## 启动服务

1. 更改 docker-compose.yml 中的镜像
2. 设置`APP_FS_WEBHOOK`环境变量为你自己的飞书的`webhook`地址
3. 设置`APP_FS_SECRET`环境变量为你自己的飞书群机器人的签名校验秘钥
4. 设置`APP_FS_ALERT_TYPE`环境变量以选择机器人消息类型。有两个选项: post(富文本)、interactive(消息卡片)
5. 启动服务

```shell
docker-compose up -d
```
