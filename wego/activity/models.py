# coding=utf-8

from django.contrib.auth.models import User
from django.db import models


STATUS = (
    ('0', u"未开始"),
    ('1', u"进行中"),
    ('2', u"已结束"),
    ('3', u"已删除"),
    ('4', u"未参加"),
    ('5', u"已参加")
)


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(u"标题", max_length=20)
    summary = models.CharField(u"介绍", max_length=50)
    reward = models.IntegerField(u"奖金", default=0)
    target_step = models.IntegerField(u"目标步数", default=0)
    start_time = models.DateTimeField(u"开始时间")
    end_time = models.DateTimeField(u"结束时间")
    status = models.CharField(u"活动状态", max_length=1, choices=STATUS, default='0')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']


class ActivityJoin(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True)
    step = models.IntegerField(u"步数", default=0)
    mileage = models.FloatField(u"距离", default=0)
    altitude = models.FloatField(u"海拔", default=0)
    calorie = models.IntegerField(u"卡路里", default=0)
    fabulous = models.IntegerField(u"赞", default=0)
    is_creater = models.BooleanField(default=False)
    is_observe = models.BooleanField(default=False)
    status = models.CharField(u"活动状态", max_length=1, choices=STATUS)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
