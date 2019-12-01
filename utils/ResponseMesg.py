# -*- coding: utf-8 -*-
class RET:
    OK = "2001"
    BadRequest = "4001"
    DBError = "5001"
    Notfound = "4004"
    ServiceError = "5002"
    AuthFail = "5003"
    MethodNotAllow = "5004"


mesgMap = {
    RET.OK: u"成功",
    RET.BadRequest: u"参数缺失",
    RET.DBError: u"数据库异常",
    RET.Notfound: u"数据不存在",
    RET.ServiceError: u"服务异常",
    RET.AuthFail: u"认证失败",
    RET.MethodNotAllow: u"请求方法不被允许"
}


