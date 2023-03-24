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

from utils import gen_sign

# urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


app = Flask(__name__)

# 加载配置文件
app.config.from_object("config")


@app.before_first_request
def before_first_request():
    app.logger.setLevel(logging.INFO)


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
    feishu_alert_type = app.config.get("APP_FS_ALERT_TYPE")

    if feishu_webhook_url == None or feishu_webhook_srt == None:
        app.logger.error(
            "Please set system environment variable and try again, Require: (APP_FS_WEBHOOK、APP_FS_SECRET)"
        )
        sys.exit(1)

    # 获取时间戳和签名
    timestamp = int(datetime.datetime.now().timestamp())
    sign = gen_sign.gen_sign(timestamp, feishu_webhook_srt)

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
        warning_isfiring = output['status']
        warning_name = "当前状态: %s \n" % output['labels']['alertname']
        warning_level = output['labels']['severity']
        warning_level_text = "告警等级: %s \n" % output['labels']['severity']
        warning_instance = "告警实例: %s \n" % output['labels']['instance']
        warning_info = "告警信息: %s" % message.replace(',', '\n').replace(':', ':  ')
        warning_end_time = "结束时间: %s \n" % arrow.get(output['endsAt']).to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
        warning_start_time = "告警时间: %s \n" % arrow.get(output['startsAt']).to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
        now_time = str(datetime.datetime.now().replace(microsecond=0))
        now_time_struct = datetime.datetime.strptime(now_time, "%Y-%m-%d %H:%M:%S")
        start_time = arrow.get(output['startsAt']).to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
        start_time_struct = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        last_time = now_time_struct - start_time_struct
        warning_last_time = "持续时间: %s \n" % last_time

        if feishu_alert_type == "post":
            send_data = {
                "timestamp": timestamp,
                "sign": sign,
                "msg_type": "post",
                "content": {
                    "post": {
                        "zh_cn": {
                            "title": title,
                            "content": [
                                [
                                    {"tag": "text", "text": warning_instance},
                                    {"tag": "text", "text": warning_start_time},
                                    {"tag": "text", "text": warning_end_time},
                                    {"tag": "text", "text": warning_level_text},
                                    {"tag": "text", "text": warning_info},
                                    {"tag": "text", "text": warning_status},
                                ]
                            ],
                        }
                    }
                },
            }
        elif feishu_alert_type == "interactive":
            title = f"%s告警通知" %warning_level
            send_data = {
                "msg_type": "interactive",
                "timestamp": timestamp,
                "sign": sign,
                "card": {
                    "config": {"wide_screen_mode": True},
                    "elements": [
                        {"tag": "div","text": {"tag": "plain_text","content": warning_name,"lines": 1},
                        "fields": [
                            {"text": {"tag": "lark_md","content": warning_instance,}},
                            {"text": {"tag": "lark_md","content": warning_info,}},
                            {"text": {"tag": "lark_md","content": warning_start_time,}},
                            {"text": {"tag": "lark_md","content": warning_last_time if warning_isfiring == 'firing' else warning_end_time,}},
                            {"text": {"tag": "lark_md","content": "<at id=all></at>" if warning_isfiring == 'firing' and warning_level == 'P0' else ""}}
                            ]
                        }
                    ],
                    "header": {
                        "template": 'red' if warning_isfiring == 'firing' and warning_level == 'P0' else 'orange' if warning_isfiring == 'firing' and warning_level == 'P1' else 'yellow' if warning_isfiring == 'firing' else 'green',
                        "title": {"content": title if warning_isfiring == 'firing' else '告警恢复',"tag": "plain_text"}
                    }
                }
            }

        try:
            # 利用 requests封装好的方法来设置http请求的重试次数
            session = requests.Session()
            session.mount('http://', HTTPAdapter(max_retries=3))
            session.mount('https://', HTTPAdapter(max_retries=3))
            send_data = json.dumps(send_data)
            session.post(feishu_webhook_url, data=send_data, headers=headers, timeout=5, verify=False)
        except requests.exceptions.RequestException as e:
            app.logger.error(e)

    return 'ok'


if __name__ == '__main__':
    app.logger.info("Prometheus Python webhook start...")
    app.run(host=app.config.get("APP_HOST"), port=int(app.config.get("APP_PORT")), debug=app.config.get("DEBUG"))
