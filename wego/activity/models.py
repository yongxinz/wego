# coding=utf-8
import uuid

from django.contrib.auth.models import User
from django.db import models
import django.utils.timezone as timezone

from tools.helper import Helper


STATUS = (
    ('CIM', u"已提交"),
    ('ONL', u"已上线"),
    ('FIN', u"已结束"),
    ('DEL', u"已删除"),
    ('OBS', u"已观战"),
    ('JOI', u"已参加")
)

ACTIVITY_TYPE = (
    ('D', u"日活动"),
    ('W', u"周活动"),
    ('C', u"自定义")
)


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(u"标题", max_length=20)
    summary = models.CharField(u"介绍", max_length=50)
    reward = models.IntegerField(u"奖金", default=0)
    target_step = models.IntegerField(u"目标步数", default=0)
    status = models.CharField(u"活动状态", max_length=5, choices=STATUS, default='ONL')
    type = models.CharField(u"活动类型", max_length=5, choices=ACTIVITY_TYPE, default='D')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']


def title_pic_path(instance, file):
    now = Helper.get_safe_now()
    return 'static/title-pic/{0}/{1}'.format(str(now.year) + str(now.month), uuid.uuid4())


class TitlePic(models.Model):
    """
    活动图片
    """
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True)
    pic = models.ImageField(upload_to=title_pic_path, default='')
    status = models.CharField(u"状态", max_length=5, choices=STATUS, default='CIM')
    created_time = models.DateTimeField(u"创建时间", auto_now_add=True)

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
    start_time = models.DateTimeField(u"开始时间", default=timezone.now)
    end_time = models.DateTimeField(u"结束时间", default=timezone.now)
    status = models.CharField(u"活动状态", max_length=5, choices=STATUS, default='JOI')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
