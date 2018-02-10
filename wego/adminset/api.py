# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets

from adminset.serializers import UsersSerializer
from adminset.models import Users
from tools.rest_helper import YMMixin


class UsersViewSet(YMMixin, viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
