# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers

from adminset.models import Users, DataDefine, SummaryPic


class UsersSerializer(serializers.ModelSerializer):
    mobile = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Users
        exclude = ('user', )


class DataDefineSerializer(serializers.ModelSerializer):
    type_display = serializers.ReadOnlyField(source='get_type_display')
    status = serializers.ReadOnlyField()

    class Meta:
        model = DataDefine
        exclude = ('created_time',)


class SummaryPicSerializer(serializers.ModelSerializer):

    class Meta:
        model = SummaryPic
        exclude = ('created_time',)
