# coding=utf-8

from rest_framework import serializers

from .models import DayData


class DayDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = DayData
        exclude = ('user', 'created_time')
