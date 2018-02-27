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

    @list_route(methods=['post'])
    def nickname(self, request):
        mobile = self.request.data.get('mobile')
        user_info = self.request.data.get('userInfo')
        
        if user_info is None:
            return Response({'status': False})

        nickname = user_info.get('nickName')
        avatar_url = user_info.get('avatarUrl')
        gender = user_info.get('gender')

        user = User.objects.get(username=mobile)
        Users.objects.filter(user=user).update(nickname=nickname, avatar_url=avatar_url, gender=gender)

        return Response({'status': True})


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
