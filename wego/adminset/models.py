# coding=utf-8

from django.db import models
from django.contrib.auth.models import User


GENDER = (
    ('0', u"女"),
    ('1', u"男")
)

TYPE = (
    ('K', u"里程"),
    ('S', u"步数")
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
    reference_value = models.DecimalField(u"参考物数值", default=0, max_digits=25, decimal_places=2, )
    summary = models.CharField(u'分享文案', max_length=100, default='')
    created_time = models.DateTimeField(u"注册时间", auto_now_add=True)

    class Meta:
        ordering = ['-id']
