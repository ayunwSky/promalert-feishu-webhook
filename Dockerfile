FROM python:3.11.2
LABEL Author="Allen_Jol"

ENV PYTHONIOENCODING=utf-8 \
    TZ=Asia/Shanghai \
    DEBIAN_FRONTEND=noninteractive

RUN mkdir -p /data/feishu-webhook

WORKDIR /data/feishu-webhook

COPY src/ .

RUN pip install --no-cache-dir -r /data/feishu-webhook/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && apt install -y tzdata \
    && chmod +x /data/feishu-webhook/startApp.sh \
    && rm -rf /etc/localtime \
    && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8080

# 一定要用双引号不要用单引号.用单引号就一直提示你找不到改脚本
CMD ["/data/feishu-webhook/startApp.sh"]
