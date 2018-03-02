# coding=utf-8

from django.db import models
from django.contrib.auth.models import User


GENDER = (
    ('0', u"女"),
    ('1', u"男")
)

TYPE = (
    ('M', u"里程(km)"),
    ('S', u"步数"),
    ('C', u"卡路里")
)

STATUS = (
    ('CIM', u"已提交"),
    ('DEL', u"已删除"),
    ('ONL', u"已上架"),
)


class Users(models.Model):
    """
    个人信息
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(u"性别", max_length=1, choices=GENDER, default='')
    nickname = models.CharField(u'微信昵称', max_length=20, default='')
    avatar_url = models.CharField(u'微信头像', max_length=300, default='')
    autograph = models.CharField(u'签名', max_length=50, default='')
    target = models.IntegerField(u'每日步数目标', default=6000)
    created_time = models.DateTimeField(u"注册时间", auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.user.username


class DataDefine(models.Model):
    """
    运动数据定义
    """
    type = models.CharField(u"数据类型", max_length=1, choices=TYPE, default='K')
    min_value = models.IntegerField(u'数据分级小', default=0)
    max_value = models.IntegerField(u'数据分级大', default=0)
    reference = models.CharField(u'参考物', max_length=10, default='')
    reference_value = models.FloatField(u"参考物数值", default=0)
    summary = models.CharField(u'分享文案', max_length=100, default='')
    status = models.CharField(u"状态", max_length=5, choices=STATUS, default='ONL')
    created_time = models.DateTimeField(u"注册时间", auto_now_add=True)

    class Meta:
        ordering = ['-id']
