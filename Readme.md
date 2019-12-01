### 通知接口
* 邮件
* 短信
* 电话
* 企业微信机器人
* 企业微信APP
* 钉钉机器人

### 运行APP
```bash
gunicorn NoticeSystem:app -c gunicorn.conf
```

### 坑
* flask获取header的参数不能使用下划线，只能使用中划线，不支持语法糖

### 邮件
```bash
curl 0.0.0.0:5001/send_mail -H "HTTP_VERIFICATION_KEY:5hbfJTAo9SBOb" -X POST -d "{'ReceiverList':'a@gmail.com,b@163.com','Subject':'测试主题','Content':'测试邮件内容2'}"
```

### 企业微信机器人
```bash
curl 0.0.0.0:5001/send_qywx_robot -H "HTTP_VERIFICATION_KEY:5hbfJTAo9SBOb" -X POST -d "{'RobotKey':'lb6test1','Content':'测试','MesgType':'markdown'}"
```

### 企业微信应用
```bash
curl 0.0.0.0:5001/send_qywx_app -H "HTTP_VERIFICATION_KEY:5hbfJTAo9SBOb" -X POST -d "{'AppName':'SREAlert','Content':'测试企业微信应用告警'}"
```
