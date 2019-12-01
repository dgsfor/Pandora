#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
import requests

RobotKeyList = {
    "lb6test1":(('key','********************'),),
    "lb6test2":(('key','********************'),), 
}


headers = {
    'Content-Type': 'application/json',
}


def PushMesg(RobotKey,Content,MesgType):
    sendMesg = {
        "msgtype": MesgType,
        MesgType: {
            "content": Content,
        }
    }
    requests.post("https://qyapi.weixin.qq.com/cgi-bin/webhook/send", headers=headers, params=RobotKeyList[RobotKey],data=json.dumps(sendMesg))
