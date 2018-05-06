# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dateutil import tz

from django.http import HttpResponse
from django.utils import timezone as datetime
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route

from .models import Activity, TitlePic, ACTIVITY_TYPE, ActivityJoin
from .serializers import ActivitySerializer, TitlePicSerializer, ActivityJoinSerializer
from .filter import ActivityJoinFilter
from tools.rest_helper import YMMixin


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
    filter_class = ActivityJoinFilter

    # def get_queryset_distinct(self):
    #     queryset = super(ActivityJoinViewSet, self).get_queryset()
    #     queryset = queryset.distinct('activity', 'start_time', 'end_time').order_by('start_time')
    #
    #     return queryset
    #
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset_distinct())
    #     # queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     serializer = self.get_serializer(page, many=True)
    #     rsp = self.get_paginated_response(serializer.data)
    #
    #     return rsp

    @list_route(methods=['get'])
    def personal(self, request):
        try:
            obj = ActivityJoin.objects.get(user=self.request.user, start_time__lte=datetime.now(), end_time__gte=datetime.now())
            start_time = obj.start_time.astimezone(tz.gettz(settings.TIME_ZONE))
            end_time = obj.end_time.astimezone(tz.gettz(settings.TIME_ZONE))
            fabulous = obj.fabulous

            obj_ = Activity.objects.get(id=obj.activity.pk)
            target = obj_.target_step
            count = ActivityJoin.objects.filter(activity=obj.activity, start_time__lte=datetime.now(), end_time__gte=datetime.now()).distinct(
                'user').count()
            reward = obj_.reward * count
        except:
            start_time = ''
            end_time = ''
            fabulous = 0
            reward = 0
            target = ''

        return Response({'results': {'start_time': start_time, 'end_time': end_time, 'fabulous': fabulous, 'reward': reward,
                                     'target': target}})
