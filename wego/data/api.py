# coding=utf-8

import time
import datetime

from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route

from adminset.models import DataDefine
from data.models import DayData
from passport.models import WeixinUsers
from data.serializers import DayDataSerializer
from tools.wx_helper import WXBizDataCrypt
from tools.business_helper import generate_summary


class WeRunViewSet(viewsets.ModelViewSet):
    queryset = DayData.objects.all()
    serializer_class = DayDataSerializer

    def get_queryset(self):
        queryset = DayData.objects.filter(created_time=datetime.datetime.now().date()).order_by('step')

        return queryset

    @list_route(methods=['get'])
    def today(self, request):
        obj = DayData.objects.filter(user=self.request.user).first()
        mileage = obj.mileage
        calorie = obj.calorie

        mileage_summary_list = []
        calorie_summary_list = []
        define_obj = DataDefine.objects.filter(status='ONL')
        for item in define_obj:
            if item.type == 'M' and item.min_value <= mileage and item.max_value > mileage:
                mileage_summary_list.append({'reference_value': item.reference_value, 'summary': item.summary})
            elif item.type == 'C' and item.min_value <= calorie and item.max_value > calorie:
                calorie_summary_list.append({'reference_value': item.reference_value, 'summary': item.summary})

        mileage_summary = generate_summary(mileage_summary_list, mileage)
        calorie_summary = generate_summary(calorie_summary_list, calorie)

        return Response({'results': {'step': obj.step, 'mileage': mileage, 'calorie': calorie,
                                     'mileage_summary': mileage_summary, 'calorie_summary': calorie_summary}})

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
            step = item['step']
            mileage = round(step * settings.TO_MILE / 1000, 2)
            calorie = round(step / settings.TO_KCAL)
            DayData.objects.update_or_create(user=wx_user.user,
                                             created_time=time.strftime('%Y-%m-%d', time.localtime(item['timestamp'])),
                                             defaults={'step': step, 'mileage': mileage, 'calorie': calorie})
