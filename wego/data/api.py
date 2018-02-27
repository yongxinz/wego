# coding=utf-8

import time
import datetime

from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response

from data.models import DayData
from passport.models import WeixinUsers
from data.serializers import DayDataSerializer
from tools.wx_helper import WXBizDataCrypt


class WeRunViewSet(viewsets.ModelViewSet):
    queryset = DayData.objects.all()
    serializer_class = DayDataSerializer

    def get_queryset(self):
        queryset = DayData.objects.filter(created_time=datetime.datetime.now().date()).order_by('step')

        return queryset

    def perform_create(self, serializer):
        crypt_data = self.request.data.get('encryptedData', '')
        iv = self.request.data.get('iv', '')

        sid = self.request.META.get('HTTP_AUTHORIZATION', 'whoareyou')
        try:
            wx_user = WeixinUsers.objects.get(sid=sid, is_del=False)
            s_key = wx_user.skey
        except:
            return Response({'status': False, 'msg': u'微信验证失败，请重新授权'})

        app_id = settings.WEIXIN.get('id')
        werun_data = WXBizDataCrypt(app_id, s_key).decrypt(crypt_data, iv)

        step_info_list = werun_data['stepInfoList']
        for item in step_info_list:
            DayData.objects.update_or_create(user=wx_user.user,
                                             created_time=time.strftime('%Y-%m-%d', time.localtime(item['timestamp'])),
                                             defaults={'step': item['step']})
