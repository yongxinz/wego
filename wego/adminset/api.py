# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, StreamingHttpResponse

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route

from adminset.serializers import UsersSerializer, DataDefineSerializer, SummaryPicSerializer
from adminset.models import Users, DataDefine, TYPE, SummaryPic
from tools.rest_helper import YMMixin


class UsersViewSet(YMMixin, viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def get_queryset(self):
        queryset = Users.objects.filter(user=self.request.user)

        return queryset

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

    @detail_route(methods=['get'])
    def get_pic(self, request, pk=None):
        queryset = SummaryPic.objects.exclude(status='DEL')

        if pk:
            pic = queryset.get(pk=pk).pic
            if pic:
                image = open(pic.url, 'rb')
                data = image.read()
                image.close()
                return Response(data, content_type="image/png")

        return Response(status=status.HTTP_404_NOT_FOUND)


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
