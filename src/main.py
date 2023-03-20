#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# *******************************************
# -*- CreateTime  :  2023/03/15 09:55:22
# -*- Author      :  Allen_Jol
# -*- FileName    :  main.py
# *******************************************

import sys
import json
import requests
import arrow
import logging
import datetime
import urllib3
from requests.adapters import HTTPAdapter
from flask import Flask, request, jsonify
import base64
import hashlib
import hmac

# urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# 加载配置文件
app.config.from_object("config")


@app.before_first_request
def before_first_request():
    app.logger.setLevel(logging.INFO)


# 健康检查接口
@app.route('/healthz', methods=['GET'])
def healch_check():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {"time": current_time, "status": "OK", "status_code": 200}
    return jsonify(data)


@app.route('/send', methods=['POST'])
def send():
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    feishu_webhook_url = app.config.get("APP_FS_WEBHOOK")
    feishu_webhook_srt = app.config.get("APP_FS_SECRET")

    if feishu_webhook_url == None or \
        feishu_webhook_srt == None:
        app.logger.error("Please set system environment variable and try again, Require: (APP_FS_WEBHOOK、APP_FS_SECRET)")
        sys.exit(1)

    timestamp = int(datetime.datetime.now().timestamp())
    string_to_sign = '{}\n{}'.format(timestamp, feishu_webhook_srt)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    data = json.loads(request.data)
    app.logger.info(data)
    alerts = data['alerts']
    for output in alerts:
        try:
            message = output['annotations']['message']
        except KeyError:
            try:
                message = output['annotations']['description']
            except KeyError:
                message = 'null'
                app.logger.error(f"Cnt not get any alert info, message is {message}")

        title = f"新平台监控告警通知: {output['labels']['alertname']}"
        warning_status = "当前状态: %s \n" % output['status']
        warning_level = "告警等级: %s \n" % output['labels']['severity']
        warning_instance = "告警实例: %s \n" % output['labels']['instance']
        warning_info = "告警信息: %s" % message.replace(',', '\n').replace(':', ':  ')
        warning_end_time = "结束时间: %s \n" % arrow.get(output['endsAt']).to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
        warning_start_time = "告警时间: %s \n" % arrow.get(output['startsAt']).to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')

        send_data = {
            "msg_type": "post",
            "sign": sign,
            "content": {
                "post": {
                    "zh_cn": {
                        "title":
                        title,
                        "content": [[{
                            "tag": "text",
                            "text": warning_instance
                        }, {
                            "tag": "text",
                            "text": warning_start_time
                        }, {
                            "tag": "text",
                            "text": warning_end_time
                        }, {
                            "tag": "text",
                            "text": warning_level
                        }, {
                            "tag": "text",
                            "text": warning_info
                        }, {
                            "tag": "text",
                            "text": warning_status
                        }]]
                    }
                }
            }
        }
        send_data = json.dumps(send_data)
        print(send_data)

        try:
            # 利用 requests封装好的方法来设置http请求的重试次数
            session = requests.Session()
            session.mount('http://', HTTPAdapter(max_retries=3))
            session.mount('https://', HTTPAdapter(max_retries=3))
            resp = session.post(feishu_webhook_url, data=send_data, headers=headers, timeout=5, verify=False)
            result = resp.json()
            print(result)
        except requests.exceptions.RequestException as e:
            app.logger.error(e)

    return 'ok'


if __name__ == '__main__':
    app.logger.info("Prometheus Python webhook start...")
    app.run(host=app.config.get("APP_HOST"), port=int(app.config.get("APP_PORT")), debug=app.config.get("DEBUG"))
