# coding=utf-8

import base64
import hashlib
import json

import datetime

import arrow
import os
import requests
from Crypto.Cipher import AES
from django.conf import settings

from passport.models import AccessToken


class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            return False

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


def check_wx_req(request):
    """
    微信公众平台接入验证
    """
    signature = request.GET.get("signature", "")
    timestamp = request.GET.get("timestamp", "")
    nonce = request.GET.get("nonce", "")

    l = [settings.WX_CONF.get('wx_Token'), timestamp, nonce]
    l.sort()
    tmp_str = hashlib.sha1(''.join(l)).hexdigest()

    return tmp_str == signature


def get_safe_now():
    try:
        from django.utils.timezone import utc
        if settings.USE_TZ:
            return datetime.datetime.utcnow().replace(tzinfo=utc)
    except:
        pass

    return datetime.datetime.now()


def send_requests_only_wx(url_path, method, params=None, data=None):
    """
    请求微信公众平台接口
    """
    wx = settings.WX_CONF
    app_id = wx.get('wx_AppId')
    secret = wx.get('wx_Secret')
    host = wx.get('wx_ApiUrl')

    url = ''.join([host, url_path])

    params.update({
        "appid": app_id,
        "secret": secret,
    })

    if method == 'GET':
        return requests.get(url, params=params, data=data)

    if method == 'POST':
        return requests.post(url, params=params, data=json.dumps(data))


def get_access_token():
    """
    获取access_token
    :return: access_token or False
    """
    try:
        access_token = AccessToken.objects.filter(expiration__gt=get_safe_now(), source='applet').values_list(
            'access_token', flat=True)
    except:
        access_token = ''

    if access_token:
        return ''.join(access_token)
    else:
        url_path = "/cgi-bin/token"
        params = {"grant_type": 'client_credential'}

        r = send_requests_only_wx(url_path, method='GET', params=params)
        if r.json().get('errmsg'):
            return False
        else:
            access_token = r.json().get('access_token')
            AccessToken.objects.create(access_token=access_token)
            return access_token


def get_online_kf_list():
    """
    获取在线客服接待信息
    :return: 返回是否有客服在线 True or False
    """
    url_path = "/cgi-bin/customservice/getonlinekflist"
    access_token = get_access_token()
    if access_token:
        params = {'access_token': access_token}
        r = send_requests_only_wx(url_path, method='GET', params=params)
        if r.json().get('kf_online_list'):
            return True

    return False


class WXHelper:
    def __init__(self):
        self.app_id = settings.WEIXIN.get('id')
        self.app_key = settings.WEIXIN.get('key')
        self.app_url = settings.WEIXIN.get('url')

    def get_token(self):
        r = AccessToken.objects.filter(expiration__gt=get_safe_now(), source='applet').values_list('access_token',
                                                                                                   flat=True)
        if r:
            access_token = ''.join(r)
        else:
            access_token = self._get_token()
            AccessToken.objects.create(access_token=access_token, source='applet')

        return access_token

    def get_appcode(self, page='pages/welcome/index', scene='123456'):
        wxapi_appcode = self.app_url + '/wxa/getwxacodeunlimit'
        params = {'access_token': self.get_token()}
        return requests.post(wxapi_appcode, params=params, json={'page': page, 'scene': scene})

    def _get_token(self):
        # 获得 access_token
        wxapi_token = self.app_url + "/cgi-bin/token"
        params = {'grant_type': 'client_credential', 'appid': self.app_id, 'secret': self.app_key}
        return requests.get(wxapi_token, params=params).json().get('access_token', '')


class XMLParseMessageTemplate:
    """提供提取消息格式中的密文及生成回复消息格式的接口"""

    # xml消息模板 转发到客服
    MESSAGE_SERVICE_RESPONSE_TEMPLATE = """<xml>
                                                <ToUserName><![CDATA[%(ToUserName)s]]></ToUserName>
                                                <FromUserName><![CDATA[%(FromUserName)s]]></FromUserName>
                                                <CreateTime>%(CreateTime)d</CreateTime>
                                                <MsgType><![CDATA[transfer_customer_service]]></MsgType>
                                            </xml>
                                        """
    # xml消息模板 直接回复
    MESSAGE_CONTENT_RESPONSE_TEMPLATE = """<xml>
                                                <ToUserName><![CDATA[%(ToUserName)s]]></ToUserName>
                                                <FromUserName><![CDATA[%(FromUserName)s]]></FromUserName>
                                                <CreateTime>%(CreateTime)d</CreateTime>
                                                <MsgType><![CDATA[%(MsgType)s]]></MsgType>
                                                <Content><![CDATA[%(Content)s]]></Content>
                                            </xml>
                                        """

    def generate(self, context):
        # 生成xml消息
        if context.get('Content'):
            resp_xml = self.MESSAGE_CONTENT_RESPONSE_TEMPLATE % context
        else:
            resp_xml = self.MESSAGE_SERVICE_RESPONSE_TEMPLATE % context

        return resp_xml


def main():
    appId = 'wx4f4bc4dec97d474b'
    sessionKey = 'tiihtNczf5v6AKRyjwEUhQ=='
    encryptedData = 'CiyLU1Aw2KjvrjMdj8YKliAjtP4gsMZMQmRzooG2xrDcvSnxIMXFufNstNGTyaGS9uT5geRa0W4oTOb1WT7fJlAC+oNPdbB+3hVbJSRgv+4lGOETKUQz6OYStslQ142dNCuabNPGBzlooOmB231qMM85d2/fV6ChevvXvQP8Hkue1poOFtnEtpyxVLW1zAo6/1Xx1COxFvrc2d7UL/lmHInNlxuacJXwu0fjpXfz/YqYzBIBzD6WUfTIF9GRHpOn/Hz7saL8xz+W//FRAUid1OksQaQx4CMs8LOddcQhULW4ucetDf96JcR3g0gfRK4PC7E/r7Z6xNrXd2UIeorGj5Ef7b1pJAYB6Y5anaHqZ9J6nKEBvB4DnNLIVWSgARns/8wR2SiRS7MNACwTyrGvt9ts8p12PKFdlqYTopNHR1Vf7XjfhQlVsAJdNiKdYmYVoKlaRv85IfVunYzO0IKXsyl7JCUjCpoG20f0a04COwfneQAGGwd5oa+T8yO5hzuyDb/XcxxmK01EpqOyuxINew=='
    iv = 'r7BXXKkLb8qrSNn05n0qiA=='

    pc = WXBizDataCrypt(appId, sessionKey)

    print(pc.decrypt(encryptedData, iv))


if __name__ == '__main__':
    main()
