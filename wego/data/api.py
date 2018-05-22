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
from activity.models import Activity, ActivityJoin
from data.serializers import DayDataSerializer
from tools.wx_helper import WXBizDataCrypt


class WeRunViewSet(viewsets.ModelViewSet):
    queryset = DayData.objects.all()
    serializer_class = DayDataSerializer

    @list_route(methods=['get'])
    def ranking(self, request):
        queryset = DayData.objects.filter(created_time=datetime.now().date()).order_by('-step')[0:100]
        serializer = self.get_serializer(queryset, many=True)

        return Response({'results': serializer.data})

    @list_route(methods=['get'])
    def today(self, request):
        obj = DayData.objects.filter(user=self.request.user).first()
        step = obj.step
        mileage = obj.mileage
        calorie = obj.calorie

        obj_m = DataDefine.objects.filter(status='ONL', type='M', min_value__lte=mileage, max_value__gt=mileage)
        if obj_m.exists():
            obj_m = obj_m.order_by('?')[:1]
            mileage_summary = obj_m[0].summary.replace('N', str(round(mileage / obj_m[0].reference_value, 2)))
        else:
            mileage_summary = '相当于' + str(round(mileage / 0.4, 2)) + '圈400米跑道'

        obj_c = DataDefine.objects.filter(status='ONL', type='C', min_value__lte=calorie, max_value__gt=calorie)
        if obj_c.exists():
            obj_c = obj_c.order_by('?')[:1]
            calorie_summary = obj_c[0].summary.replace('N', str(round(mileage / obj_c[0].reference_value, 2)))
        else:
            calorie_summary = '相当于' + str(round(calorie / 80, 2)) + '个苹果'

        # 参加活动相关
        id, reward, is_join = '', 0, False
        target = self.request.auth.target

        if ActivityJoin.objects.filter(user=self.request.user, start_time__lte=datetime.now(), end_time__gte=datetime.now(), status='JOI').exists():
            is_join = True

            obj = ActivityJoin.objects.get(user=self.request.user, start_time__lte=datetime.now(), end_time__gte=datetime.now(), status='JOI')

            obj_ = Activity.objects.get(id=obj.activity.pk)
            id = obj_.id
            target = obj_.target_step
            count = ActivityJoin.objects.filter(activity=obj.activity, start_time__lte=datetime.now(),
                                                end_time__gte=datetime.now(), status='JOI').count()
            reward = obj_.reward * count

        return Response({'results': {'step': step, 'target': target, 'mileage': mileage, 'calorie': calorie,
                                     'mileage_summary': mileage_summary, 'calorie_summary': calorie_summary,
                                     'reward': reward, 'id': id, 'is_join': is_join}})

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
