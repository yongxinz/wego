# coding=utf-8

from rest_framework import serializers

from .models import DataSummary


class DataSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = DataSummary
        exclude = ('user', 'created_time')
