# coding=utf-8

from rest_framework import serializers

from .models import DayData


class DayDataSerializer(serializers.ModelSerializer):
    user_info = serializers.ReadOnlyField(source='get_user_info')

    class Meta:
        model = DayData
        exclude = ('user', 'created_time')
