# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route

from .models import Activity, TitlePic, ACTIVITY_TYPE
from .serializers import ActivitySerializer, TitlePicSerializer
from tools.rest_helper import YMMixin


class ActivityViewSet(YMMixin, viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

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
