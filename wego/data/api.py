# coding=utf-8

import time
from datetime import datetime, timedelta

from django.conf import settings
from django.utils.timezone import get_current_timezone
from django.db.models import Sum
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
        queryset = DayData.objects.filter(created_time=datetime.now().date()).order_by('step')

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
                mileage_summary_list.append({'reference_value': item.reference_value, 'summary': item.summary,
                                             'id': item.id})
            elif item.type == 'C' and item.min_value <= calorie and item.max_value > calorie:
                calorie_summary_list.append({'reference_value': item.reference_value, 'summary': item.summary,
                                             'id': item.id})

        if mileage_summary_list:
            id, mileage_summary = generate_summary(mileage_summary_list, mileage)
        else:
            mileage_summary = ''
        if calorie_summary_list:
            id, calorie_summary = generate_summary(calorie_summary_list, calorie)
        else:
            calorie_summary = ''

        return Response({'results': {'step': obj.step, 'mileage': mileage, 'calorie': calorie,
                                     'mileage_summary': mileage_summary, 'calorie_summary': calorie_summary,
                                     'target': self.request.auth.target}})

    @list_route(methods=['get'])
    def personal(self, request):
        now = datetime.now()
        timezone = get_current_timezone()
        month_begin = datetime(now.year, now.month, 1).replace(tzinfo=timezone)
        week_first_day = now - timedelta(days=now.weekday())
        week_begin = datetime(week_first_day.year, week_first_day.month, week_first_day.day).replace(tzinfo=timezone)

        # 日数据
        obj_day = DayData.objects.filter(user=self.request.user).first()
        step_day = obj_day.step
        mileage_day = obj_day.mileage

        # 周数据
        obj_week = DayData.objects.filter(
            user=self.request.user, created_time__gte=week_begin).aggregate(
            step=Sum('step'), mileage=Sum('mileage'))

        step_week = obj_week.get('step')
        mileage_week = obj_week.get('mileage')

        # 月数据
        obj_month = DayData.objects.filter(
            user=self.request.user, created_time__gte=month_begin).aggregate(
            step=Sum('step'), mileage=Sum('mileage'))

        step_month = obj_month.get('step')
        mileage_month = obj_month.get('mileage')

        return Response({'results': {'step_day': step_day, 'mileage_day': mileage_day,
                                     'step_week': step_week, 'mileage_week': mileage_week,
                                     'step_month': step_month, 'mileage_month': mileage_month}})

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
