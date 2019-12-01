# -*- coding: utf-8 -*-

import json,requests
from .secret import QYWXAPPKEY

"""
获取access token,token的有效期为两个小时
"""
def get_access_token(appsec):
    ACCESS_TOKEN_URL = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (QYWXAPPKEY["WX_CORPID"], appsec)
    try:
        result = requests.get(ACCESS_TOKEN_URL)
        result = result.json()
    except Exception as e:
        return None
    access_token = result.get('access_token')
    return access_token

"""
向应用中发送消息
注：目前只支持textcard消息类型，有需要其他类型的可以参考这里，并自己撸一把。https://work.weixin.qq.com/api/doc#90000/90135/90236
注：企业可以分组，涉及到分组发送的话可以修改touser参数
"""
def SendWxAPP(appname,content,touser="@all"):
    token = get_access_token(QYWXAPPKEY["APPSecret"][appname]["appsec"])
    if not token:
        raise Exception("access token is None")
    data = {
        "touser":touser,
        "toparty":"",
        "totag": "",
        "msgtype": "textcard",
        "agentid":int(QYWXAPPKEY["APPSecret"][appname]["agentid"]),
        "textcard":{
            "title":"XX告警通知",
            "description":content,
            "url":"https://www.baidu.com",
            "btntxt": "点击查看告警信息"
        },
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
    }
    rsp = requests.post("https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % token,data=json.dumps(data))
    return rsp.text