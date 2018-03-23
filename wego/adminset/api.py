# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.conf import settings

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route

from adminset.serializers import UsersSerializer, DataDefineSerializer, SummaryPicSerializer
from adminset.models import Users, DataDefine, TYPE, SummaryPic
from tools.rest_helper import YMMixin


class UsersViewSet(YMMixin, viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    @list_route(methods=['get'])
    def all(self, request):
        queryset = Users.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = UsersSerializer(page, many=True)
        rsp = self.get_paginated_response(serializer.data)

        return rsp

    @detail_route(methods=['patch', 'put'])
    def nickname(self, request, pk):
        user_info = self.request.data.get('userInfo')
        
        if user_info is None:
            return Response({'status': False})

        nickname = user_info.get('nickName')
        avatar_url = user_info.get('avatarUrl')
        gender = user_info.get('gender')

        obj = self.get_object()
        obj.nickname = nickname
        obj.avatar_url = avatar_url
        obj.gender = gender
        obj.save()

        return Response({'status': True})

    @detail_route(methods=['patch', 'put'])
    def target(self, request, pk):
        obj = self.get_object()
        obj.target = self.request.data.get('target')
        obj.save()

        return Response({
            'status': True,
            'success_msg': u'设置目标成功!'
        })


class DataDefineViewSet(YMMixin, viewsets.ModelViewSet):
    queryset = DataDefine.objects.all()
    serializer_class = DataDefineSerializer

    @list_route()
    def type(self, request):
        result = []
        for option in TYPE:
            option_group = {'label': option[1], 'value': option[0]}
            result.append(option_group)
        return Response(result)

    @list_route()
    def summary(self, request):
        item = self.request.query_params.get('item', '')
        type = self.request.query_params.get('type', '')

        define_obj = DataDefine.objects.filter(status='ONL', type=type, min_value__lte=item, max_value__gt=item)
        if define_obj.exists():
            define_obj = define_obj.order_by('?')[:1]

            obj = SummaryPic.objects.filter(data_define=define_obj[0].id).exclude(status='DEL').order_by('?')[:1]
            summary_pic_id = obj[0].id
        else:
            summary_pic_id = 6

        return Response({'results': {'url': settings.DEFAULT_URL + 'get_pic/?pk=' + str(summary_pic_id)}})

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


class SummaryPicViewSet(YMMixin, viewsets.ModelViewSet):
    queryset = SummaryPic.objects.all()
    serializer_class = SummaryPicSerializer

    def get_queryset(self):
        queryset = SummaryPic.objects.exclude(status='DEL')

        data_define = self.request.query_params.get('data_define')
        if data_define:
            queryset = queryset.filter(data_define=data_define)

        return queryset


def get_pic(request):
    pk = request.GET.get('pk')
    queryset = SummaryPic.objects.exclude(status='DEL')

    if pk:
        pic = queryset.get(pk=pk).pic
        image = open(pic.url, 'rb')
        data = image.read()
        image.close()
        return HttpResponse(data, content_type="image/png")

    return HttpResponse({}, content_type="image/png")
