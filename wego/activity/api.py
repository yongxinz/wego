# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dateutil import tz
import time
import uuid
import requests

from django.http import HttpResponse
from django.utils import timezone as datetime
from django.conf import settings
from django.db.models import Q, Sum, Value
from django.db.models.functions import Coalesce
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route

from adminset.models import Users
from data.models import DayData
from .models import Activity, TitlePic, ACTIVITY_TYPE, ActivityJoin, Fabulous
from .serializers import ActivitySerializer, TitlePicSerializer, ActivityJoinSerializer, FabulousSerializer
# from .filter import ActivityJoinFilter
from tools.rest_helper import YMMixin
from tools.helper import Dict2obj, dict_to_xml, xml_to_dict, generate_sign


class ActivityViewSet(YMMixin, viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    @list_route(methods=['get'])
    def all(self, request):
        queryset = Activity.objects.filter(status='ONL')
        serializer = self.get_serializer(queryset, many=True)
        return Response({'results': serializer.data})

    @list_route()
    def type(self, request):
        result = []
        for option in ACTIVITY_TYPE:
            option_group = {'label': option[1], 'value': option[0]}
            result.append(option_group)
        return Response(result)

    @detail_route(methods=['patch', 'put'])
    def offline(self, request, pk):
        obj = self.get_object()
        obj.status = "CIM"
        obj.save()

        return Response({
            'status': True,
            'success_msg': u'下线成功!'
        })

    @detail_route(methods=['patch', 'put'])
    def online(self, request, pk):
        obj = self.get_object()
        obj.status = "ONL"
        obj.save()

        return Response({
            'status': True,
            'success_msg': u'上线成功!'
        })

    @list_route(methods=['get'])
    def content(self, request):
        return Response({'results': settings.CONTENT})


class TitlePicViewSet(YMMixin, viewsets.ModelViewSet):
    queryset = TitlePic.objects.all()
    serializer_class = TitlePicSerializer

    def get_queryset(self):
        queryset = TitlePic.objects.exclude(status='DEL')

        activity = self.request.query_params.get('activity')
        if activity:
            queryset = queryset.filter(activity=activity)

        return queryset

    @list_route()
    def get_title_pic(self, request):
        pk = request.GET.get('pk')

        if pk:
            queryset = TitlePic.objects.exclude(status='DEL')
            pic = queryset.get(pk=pk).pic
            image = open(pic.url, 'rb')
        else:
            image = open('static/default.png', 'rb')

        data = image.read()
        image.close()
        return HttpResponse(data, content_type="image/png")


def get_title_pic(request):
    pk = request.GET.get('pk')
    queryset = TitlePic.objects.exclude(status='DEL')

    if pk:
        pic = queryset.get(pk=pk).pic
        image = open(pic.url, 'rb')
        data = image.read()
        image.close()
        return HttpResponse(data, content_type="image/png")

    return HttpResponse({}, content_type="image/png")


class ActivityJoinViewSet(YMMixin, viewsets.ModelViewSet):
    queryset = ActivityJoin.objects.all()
    serializer_class = ActivityJoinSerializer
    # filter_class = ActivityJoinFilter

    def get_queryset_distinct(self):
        queryset = super(ActivityJoinViewSet, self).get_queryset()
        queryset = queryset.distinct('activity', 'start_time', 'end_time').order_by('start_time')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset_distinct())
        # queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        rsp = self.get_paginated_response(serializer.data)

        return rsp

    @list_route(methods=['get'])
    def is_join(self, request):
        start_time = self.request.query_params.get('start_time')
        activity = self.request.query_params.get('activity')

        res = []
        obj = ActivityJoin.objects.filter((Q(status='JOI') | Q(status='OBS')), user=self.request.user, activity=activity, end_time__gt=start_time)
        for item in obj:
            res.append({'id': item.id, 'status': item.status})

        is_join = ActivityJoin.objects.filter(user=self.request.user, status='JOI', end_time__gt=start_time).exists()

        return Response({'results': res, 'is_join': is_join})

    @list_route(methods=['get'])
    def detail(self, request):
        activity = self.request.query_params.get('activity')

        try:
            pic = TitlePic.objects.get(activity=activity, status='CIM')
            pic_id = pic.id
        except:
            pic_id = ''

        time_range, status, join_id, type = '', '', '', ''
        res, dates, steps = [], [], []
        step, reward = 0, 0

        if ActivityJoin.objects.filter((Q(status='JOI') | Q(status='OBS')), user=self.request.user, activity=activity,
                                       start_time__lte=datetime.now(), end_time__gte=datetime.now()).exists():

            start_time, end_time = '', ''
            obj = ActivityJoin.objects.filter((Q(status='JOI') | Q(status='OBS')), activity=activity,
                                              start_time__lte=datetime.now(), end_time__gte=datetime.now())

            for item in obj:
                if time_range == '':
                    start_time = str(item.start_time)
                    end_time = str(item.end_time)

                    start_time_format = start_time[5:10].replace('-', '.')
                    end_time_format = end_time[5:10].replace('-', '.')
                    time_range = start_time_format + '~' + end_time_format

                if item.user == self.request.user:
                    status = item.status
                    join_id = item.id
                    type = item.activity.type

                    user = Users.objects.get(user=item.user)
                    data = DayData.objects.filter(user=item.user).first()
                    fabulous = Fabulous.objects.filter(activity_join=item.id, user_receive=item.user).count()
                    is_fabulous = Fabulous.objects.filter(activity_join=item.id, user_give=self.request.user).exists()
                    res.append({'user': user.id, 'nickname': user.nickname, 'avatar_url': user.avatar_url, 'step': data.step, 'activity_join': item.id,
                                'fabulous': fabulous, 'is_fabulous': is_fabulous, 'status': item.status})
            res.sort(key=lambda k: k['step'], reverse=True)

            obj_ = Activity.objects.get(id=activity)
            count = ActivityJoin.objects.filter(activity=activity, start_time__lte=datetime.now(), end_time__gte=datetime.now(), status='JOI').count()
            reward = obj_.reward * count

            day_data = DayData.objects.filter(user=self.request.user,
                                              created_time__range=[start_time, end_time]).values('created_time', 'step')
            for item in day_data:
                dates.insert(0, str(item['created_time'])[5:10].replace('-', '.'))
                steps.insert(0, item['step'])
                step += item['step']

        return Response({'results': {'reward': reward, 'res': res, 'pic_id': pic_id, 'time_range': time_range,
                                     'dates': dates, 'steps': steps, 'step': step, 'status': status, 'join_id': join_id, 'type': type}})

    @detail_route(methods=['patch', 'put'])
    def join(self, request, pk):
        status = self.request.data.get('status')

        obj = self.get_object()
        obj.status = status
        obj.save()

        return Response({'status': True})

    @list_route(methods=['get'])
    def summary(self, request):
        count = ActivityJoin.objects.filter((Q(status='JOI') | Q(status='FIN')), user=self.request.user).count()
        reward = ActivityJoin.objects.filter(user=self.request.user, status='FIN').aggregate(reward=Coalesce(Sum('reward'), Value(0)))

        return Response({'count': count, 'reward': reward.get('reward', 0)})

    @list_route(methods=['get'])
    def payments(self, request):
        conf = Dict2obj(settings.WEIXIN)
        data = {
            'appid': conf.id,
            'mch_id': conf.mch_id,
            'nonce_str': str(uuid.uuid4()).replace('-', ''),
            'body': 'WeGo活动费'.encode('utf-8'),
            'openid': self.request.auth.openid,
            'out_trade_no': str(int(time.time())),
            'total_fee': 1,
            'spbill_create_ip': '127.0.0.1',
            'notify_url': 'http://127.0.0.1:8810/activity/list/notify',
            'trade_type': 'JSAPI'
        }

        sign = generate_sign(data, conf.mch_key)
        data['sign'] = sign
        xml_data = dict_to_xml(data)

        response = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder', data=xml_data, headers={'Content-type': 'text/xml'})
        prepay_id = xml_to_dict(response.text).get('prepay_id')
        paySign_data = {
            'appId': data.get('appid'),
            'timeStamp': data.get('out_trade_no'),
            'nonceStr': data.get('nonce_str'),
            'package': 'prepay_id={0}'.format(prepay_id),
            'signType': 'MD5'
        }

        sign = generate_sign(paySign_data, conf.mch_key)
        paySign_data['paySign'] = sign

        return Response(paySign_data)

    @list_route(methods=['post'])
    def notify(self):
        result_data = {
            'return_code': 'SUCCESS',
            'return_msg': 'OK'
        }

        return dict_to_xml(result_data), {'Content-Type': 'application/xml'}


class FabulousViewSet(YMMixin, viewsets.ModelViewSet):
    queryset = Fabulous.objects.all()
    serializer_class = FabulousSerializer
