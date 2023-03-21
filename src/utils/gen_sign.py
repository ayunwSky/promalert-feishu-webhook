#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# *******************************************
# -*- CreateTime  :  2023/03/21 12:47:52
# -*- Author      :  Allen_Jol
# -*- FileName    :  genSign.py
# -*- Desc        :  None
# *******************************************

import hashlib
import base64
import hmac

def gen_sign(timestamp, secret):
    # 拼接 timestamp 和 secret
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode('utf-8')
    print(sign)
    return sign
