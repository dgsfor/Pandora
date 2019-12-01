# -*- coding: utf-8 -*-

import logging
from flask import Flask,Response,jsonify,request
from flask_cors import *
from utils.ResponseMesg import RET,mesgMap
from utils.secret import VERIFICATION_KEY
from utils.send_qywx_robot import *
from utils.send_mail import *
from utils.send_qywx_app import *

root_mesg = "Talk is cheap, Show me the code!"

class MyResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response,(list,dict)):
            response =  jsonify(response)
        return super(Response, cls).force_type(response,environ)

class MyFlask(Flask):
    response_class = MyResponse

app = MyFlask(__name__)
# 允许跨域
CORS(app,supports_credentials=True)

@app.route('/',methods=['GET','POST'])
def RootPath():
    return {"status": RET.OK, "mesg": mesgMap[RET.OK], "returnmesg": root_mesg}

@app.route('/send_mail',methods=['POST'])
def SendMail():
    verificationKey = request.headers.get("HTTP-VERIFICATION-KEY")
    if verificationKey != VERIFICATION_KEY["CUSTOM"]:
        return {"status": RET.AuthFail, "mesg": mesgMap[RET.AuthFail]}
    if request.method == 'POST':
        data = request.get_data()
        jsonData = eval(data)
        """
        ReceiverList 邮件接收人列表，分号(;)隔开
        Subject 邮件主题
        Content 邮件内容
        """
        ReceiverList = jsonData["ReceiverList"]
        Subject = jsonData["Subject"]
        Content = jsonData["Content"]
        if ReceiverList is None or Subject is None or Content is None:
            return {"status": RET.BadRequest, "mesg": mesgMap[RET.BadRequest],"details": "获取ReceiverList/Subject/Content参数失败"}
        SendEmail(ReceiverList,Subject,Content)
        return {"status": RET.OK, "mesg": mesgMap[RET.OK]}
    else:
        return {"status":RET.MethodNotAllow,"mesg":mesgMap[RET.MethodNotAllow]}


@app.route('/send_qywx_robot',methods=['POST'])
def SendQYEXRobot():
    verificationKey = request.headers.get("HTTP-VERIFICATION-KEY")
    if verificationKey != VERIFICATION_KEY["CUSTOM"]:
        return {"status":RET.AuthFail,"mesg":mesgMap[RET.AuthFail]}
    if request.method == 'POST':
        data = request.get_data()
        jsonData = eval(data)
        """
        robotkey 机器人名称
        content  消息内容
        mesgtype 消息类型
        """
        robotkey = jsonData["RobotKey"]
        content = jsonData["Content"]
        mesgtype = jsonData["MesgType"]
        if robotkey is None or content is None or mesgtype is None:
            return {"status": RET.BadRequest, "mesg": mesgMap[RET.BadRequest], "details": "获取RobotKey/Content/MesgType参数失败"}
        if robotkey not in RobotKeyList:
            return {"status": RET.BadRequest, "mesg": mesgMap[RET.BadRequest], "details": "请传入正确的机器人key"}
        if mesgtype not in ['text','markdown']:
            return {"status": RET.BadRequest, "mesg": mesgMap[RET.BadRequest], "details": "请选择正确的消息类型：text/markdown"}

        PushMesg(robotkey,content,mesgtype)
        return {"status": RET.OK, "mesg": mesgMap[RET.OK]}
    else:
        return {"status":RET.MethodNotAllow,"mesg":mesgMap[RET.MethodNotAllow]}

@app.route('/send_qywx_app',methods=['POST'])
def SendQYWXAPP():
    verificationKey = request.headers.get("HTTP-VERIFICATION-KEY")
    if verificationKey != VERIFICATION_KEY["CUSTOM"]:
        return {"status": RET.AuthFail, "mesg": mesgMap[RET.AuthFail]}
    if request.method == 'POST':
        data = request.get_data()
        jsonData = eval(data)
        """
        AppName 应用名称
        Content 消息内容
        """
        AppName = jsonData["AppName"]
        Content = jsonData["Content"]
        if AppName is None or Content is None:
            return {"status": RET.BadRequest, "mesg": mesgMap[RET.BadRequest],"details": "获取AppName/Content参数失败"}
        if AppName not in QYWXAPPKEY["APPSecret"]:
            return {"status": RET.BadRequest, "mesg": mesgMap[RET.BadRequest], "details": "请传入正确的应用名称"}
        SendWxAPP(AppName,Content)
        return {"status": RET.OK, "mesg": mesgMap[RET.OK]}
    else:
        return {"status": RET.MethodNotAllow, "mesg": mesgMap[RET.MethodNotAllow]}

if __name__ != '__main__':
    # 如果不是直接运行，则将日志输出到 gunicorn 中
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
