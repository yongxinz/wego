# coding=utf-8

from rest_framework import serializers
from django.utils import timezone as datetime

from .models import Activity, TitlePic, ActivityJoin, Fabulous


class ActivitySerializer(serializers.ModelSerializer):
    type_display = serializers.ReadOnlyField(source='get_type_display')
    join_status = serializers.SerializerMethodField()
    join_reward = serializers.SerializerMethodField()

    def get_join_status(self, obj):
        try:
            obj = ActivityJoin.objects.get(user=obj.user, activity=obj.id, start_time__lte=datetime.now(), end_time__gte=datetime.now())
            status = obj.status
        except:
            status = ''

        return status

    def get_join_reward(self, obj):
        count = ActivityJoin.objects.filter(activity=obj.id, start_time__lte=datetime.now(), end_time__gte=datetime.now()).distinct('user').count()

        return obj.reward * count

    class Meta:
        model = Activity
        exclude = ()


class TitlePicSerializer(serializers.ModelSerializer):

    class Meta:
        model = TitlePic
        exclude = ('created_time',)


class ActivityJoinSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source='activity.title')

    class Meta:
        model = ActivityJoin
        exclude = ()


class FabulousSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fabulous
        exclude = ('created_time',)
