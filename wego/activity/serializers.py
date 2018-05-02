# coding=utf-8

from rest_framework import serializers

from .models import Activity, TitlePic


class ActivitySerializer(serializers.ModelSerializer):
    type_display = serializers.ReadOnlyField(source='get_type_display')

    class Meta:
        model = Activity
        exclude = ('user', 'created_time')


class TitlePicSerializer(serializers.ModelSerializer):

    class Meta:
        model = TitlePic
        exclude = ('created_time',)
