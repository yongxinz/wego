#!/usr/local/bin/python
# coding=utf-8
import requests
import arrow
from django.conf import settings
from tools.helper import Dict2obj


class Sms(object):
    conf = Dict2obj(settings.SMS)
    # 服务地址
    host = conf.url
    # 创蓝账号
    account = conf.uid
    # 创蓝密码
    password = conf.key
    # 端口号
    port = 80
    # 版本号
    version = "v1.1"
    # 查账户信息的URI
    balance_get_uri = "/msg/QueryBalance"
    # 智能匹配模版短信接口的URI
    sms_send_uri = "/msg/HttpBatchSendSM"

    @classmethod
    def get_user_balance(self):
        """
        取账户余额
        """
        params = {
            'account': self.account,
            'pswd': self.password,
        }

        return requests.get(self.host + self.balance_get_uri, params=params).text

    @classmethod
    def send_sms(self, text, mobile):
        """
        能用接口发短信
        """
        params = {
            'account': self.account,
            'pswd': self.password,
            'msg': text,
            'mobile': mobile,
            'needstatus': 'false',
            'extno': '',
        }

        return requests.post(self.host + self.sms_send_uri, data=params).text


# class Ding(object):
#     @classmethod
#     def send(cls, text, group):
#         headers = {'Content-Type': 'application/json; charset=utf-8'}
#         text = {
#             "msgtype": "text",
#             "text": {
#                 "content": text
#             }
#         }
#         print requests.post(url=settings.DING.get(group), json=text, headers=headers).text


if __name__ == '__main__':
    print('请使用： python manage.py sms_send')
