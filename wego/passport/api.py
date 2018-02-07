# coding=utf-8

import uuid
import arrow
import requests

from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from rest_framework.decorators import list_route
from rest_framework import viewsets
from rest_framework.response import Response

from passport.models import WeixinUsers, AppUsers
from tools.business_helper import sms_check, send_sms_by_key, get_or_create_user
from tools.helper import Helper, Dict2obj, YMapi
from tools.wx_helper import WXBizDataCrypt, WXHelper


class WeixinUserViewSet(viewsets.ViewSet):
    permission_classes = ()

    @list_route(methods=['get'], authentication_classes=())
    def check(self, request):
        sid = request.META.get('HTTP_AUTHORIZATION', 'whoareyou')

        # 检查普通微信验证
        try:
            wx_user = WeixinUsers.objects.get(sid=sid, is_del=False)
        except:
            return Response({'status': False, 'msg': u'用户微信验证失败，请重新登录打开小程序', 'code': 403001})

        # 检查微信号是否绑定过系统用户
        if wx_user.user is None:
            return Response({'status': False, 'msg': u'没有绑定系统用户，请绑定系统用户', 'code': 403002})

        return Response(dict(status=True, user={'mobile': wx_user.user.username}, time=arrow.utcnow().for_json(), ))

    @list_route(methods=['get'], authentication_classes=())
    def login(self, request):
        # 通过微信code获取用户openid
        conf = Dict2obj(settings.WEIXIN)
        url = conf.url + "/sns/jscode2session"
        js_code = request.query_params.get('code', '')
        params = dict(appid=conf.id, secret=conf.key, js_code=js_code, grant_type="authorization_code")
        rq = requests.get(url, params=params).json()

        if rq.get('errcode'):
            return Response(dict(status=False, msg=rq))

        # 更新该微信号(openid)的sid和skey
        wx_user, is_new = WeixinUsers.objects.update_or_create(openid=rq.get('openid'), is_del=False, defaults={
            'skey': rq.get('session_key'),
            'unionid': rq.get('unionid', ''),
            'sid': uuid.uuid4(),
        })

        # 如果微信绑定过系统用户, 便写入appuser
        if wx_user.user is not None:
            AppUsers.objects.update_or_create(
                user=wx_user.user, source='wx_' + str(wx_user.pk), is_del=False, defaults={'hash_key': wx_user.sid}
            )

        return Response(dict(status=True, sid=wx_user.sid))

    @list_route(methods=['post'], authentication_classes=())
    def join2wx(self, request):
        # 检查微信登录是否成功
        sid = request.META.get('HTTP_AUTHORIZATION', 'whoareyou')
        try:
            wx_user = WeixinUsers.objects.get(sid=sid, is_del=False)
            skey = wx_user.skey
        except:
            return Response({'status': False, 'msg': u'微信验证失败，请重新授权'})

        # 解密获得用户手机号
        crypt_data = request.data.get('encryptedData', '')
        iv = request.data.get('iv', '')
        app_id = settings.WEIXIN.get('id')

        wx_info = WXBizDataCrypt(app_id, skey).decrypt(crypt_data, iv)
        if wx_info is False:
            print(111, wx_info)

        # 绑定微信用户和系统用户
        user = get_or_create_user(mobile=wx_info.get('purePhoneNumber'))
        wx_user.user = user
        wx_user.save()

        # 写入appUser 避免 切换绑定时，同一个sid绑定到多个用户
        AppUsers.objects.filter(hash_key=sid).delete()
        AppUsers.objects.update_or_create(
            user=user, source='wx_' + str(wx_user.pk), is_del=False, defaults={'hash_key': wx_user.sid}
        )

        return Response({'status': True, 'msg': u'绑定系统用户成功!', 'mobile': wx_info.get('purePhoneNumber')})

    @list_route(methods=['post'], authentication_classes=())
    def join(self, request):
        mobile = request.data.get('mobile', '')
        smscode = request.data.get('smscode', '')

        # 检查微信登录是否成功
        sid = request.META.get('HTTP_AUTHORIZATION', 'whoareyou')
        try:
            wx_user = WeixinUsers.objects.get(sid=sid, is_del=False)
        except:
            return Response({'status': False, 'msg': u'微信验证失败，请重新授权'})

        # 验证手机号格式
        mobile_status = Helper.mobile_format_check(mobile)
        if not mobile_status.get('status'):
            return Response(mobile_status)

        if not smscode:
            # 发送短信验证码
            return Response(send_sms_by_key(mobile))
        else:
            # 验证短信验证码
            if sms_check(mobile, smscode):
                user = get_or_create_user(mobile=mobile)
                wx_user.user = user
                wx_user.save()

                AppUsers.objects.filter(hash_key=sid).delete()  # 避免多次绑定导致sid重复
                AppUsers.objects.update_or_create(
                    user=user, source='wx_' + str(wx_user.pk), is_del=False, defaults={'hash_key': wx_user.sid}
                )

                return Response({
                    'status': True, 'msg': u'绑定系统用户成功!',
                    'user': {'mobile': wx_user.user.username},
                    'time': arrow.utcnow().for_json()
                })
            else:
                return Response({'status': False, 'msg': u'手机验证码错误！'})

    @list_route(methods=['get'])
    def cancel(self, request):
        sid = request.META.get('HTTP_AUTHORIZATION', 'whoareyou')

        try:
            WeixinUsers.objects.filter(sid=sid).update(user=None)
            AppUsers.objects.filter(hash_key=sid).delete()
            resp = {'msg': u'解除绑定成功', 'status': True}
        except:
            resp = {'msg': u'解除绑定失败', 'status': False}

        resp.update({'time': arrow.now().for_json()})

        return Response(resp)

    @list_route(methods=['get'], authentication_classes=())
    def applet_image(self, request):
        page = request.query_params.get('page')
        hash_key = request.query_params.get('hash_key', '').replace('-', '')

        return HttpResponse(WXHelper().get_appcode(page=page, scene=hash_key).content, content_type="image/jpeg")
