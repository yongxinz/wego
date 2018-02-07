# coding=utf-8

import time

from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response

from adminset.models import DataSummary
from passport.models import WeixinUsers
from adminset.serializers import DataSummarySerializer
from tools.wx_helper import WXBizDataCrypt


class WeRunViewSet(viewsets.ModelViewSet):
    queryset = DataSummary.objects.all()
    serializer_class = DataSummarySerializer

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
        print(werun_data)

        step_info_list = werun_data['stepInfoList']
        for item in step_info_list:
            print(time.strftime('%Y-%m-%d', time.localtime(item['timestamp'])))
            print(item['step'])
            DataSummary.objects.update_or_create(user=wx_user.user, created_time=time.strftime('%Y-%m-%d', time.localtime(item['timestamp'])),
                                                 defaults={'step': item['step']})
