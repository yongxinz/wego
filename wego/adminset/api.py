# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from django.contrib.auth.models import User

from adminset.serializers import UsersSerializer, DataDefineSerializer
from adminset.models import Users, DataDefine, TYPE
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
