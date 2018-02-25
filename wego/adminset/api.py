# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from django.contrib.auth.models import User

from adminset.serializers import UsersSerializer
from adminset.models import Users
from tools.rest_helper import YMMixin


class UsersViewSet(YMMixin, viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    @list_route(methods=['post'])
    def nickname(self, request):
        mobile = self.request.data.get('mobile')
        userInfo = self.request.data.get('userInfo')
        
        if userInfo is None:
            return Response({'status': False})

        nickname = userInfo.get('nickName')
        avatar_url = userInfo.get('avatarUrl')
        gender = userInfo.get('gender')

        user = User.objects.get(username=mobile)
        Users.objects.filter(user=user).update(nickname=nickname, avatar_url=avatar_url, gender=gender)

        return Response({'status': True})
