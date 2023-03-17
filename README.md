# promalert-feishu-webhook

python3.11 + flask 编写了一个对接飞书 API 实现告警的 webhook

## 构建镜像

```shell
docker build -t promalert-feishu-webhook:v0.0.1 .
```

## 启动服务

1. 更改 docker-compose.yml 中的镜像,设置`APP_FS_WEBHOOK`环境变量为你自己的飞书的`webhook`地址

2. 启动服务

```shell
docker-compose up -d
```
