# coding=utf-8

from django.contrib.auth.models import User
from django.db import models


STATUS = (
    ('CIM', u"已提交"),
    ('ONL', u"已上线"),
    ('FIN', u"已结束"),
    ('DEL', u"已删除"),
    ('OBS', u"已观战"),
    ('JOI', u"已参加")
)


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(u"标题", max_length=20)
    summary = models.CharField(u"介绍", max_length=50)
    reward = models.IntegerField(u"奖金", default=0)
    target_step = models.IntegerField(u"目标步数", default=0)
    start_time = models.DateField(u"开始时间")
    end_time = models.DateField(u"结束时间")
    status = models.CharField(u"活动状态", max_length=5, choices=STATUS, default='ONL')
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
    status = models.CharField(u"活动状态", max_length=5, choices=STATUS, default='JOI')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
