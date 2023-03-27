#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# *******************************************
# -*- CreateTime  :  2023/03/22 13:47:03
# -*- Author      :  Allen_Jol
# -*- FileName    :  construct_json_msg.py
# -*- Desc        :  构造富文本和消息卡片两种json数据
# *******************************************


def send_post_data(timestamp, sign, title, warning_status, warning_level, warning_instance, warning_info, warning_end_time,
                   warning_start_time):
    send_post_data = {
        "timestamp": timestamp,
        "sign": sign,
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title":
                    title,
                    "content": [[
                        {
                            "tag": "text",
                            "text": warning_instance
                        },
                        {
                            "tag": "text",
                            "text": warning_start_time
                        },
                        {
                            "tag": "text",
                            "text": warning_end_time
                        },
                        {
                            "tag": "text",
                            "text": warning_level
                        },
                        {
                            "tag": "text",
                            "text": warning_info
                        },
                        {
                            "tag": "text",
                            "text": warning_status
                        },
                    ]],
                }
            }
        },
    }

    return send_post_data


def send_interactive_data(timestamp, sign, title, warning_status, warning_level, warning_instance, warning_info,
                          warning_end_time, warning_start_time):
    pass
