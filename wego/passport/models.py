# coding=utf-8

import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class CodeDB(models.Model):
    mobile = models.CharField(max_length=15)
    sms_code = models.CharField(max_length=10)
    hash_key = models.CharField(blank=False, max_length=40, default="989997b9ea3ef632d1cf796f5e02f36dd4d31986")
    limit_times = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)


class AppUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    hash_key = models.UUIDField(u"", default=uuid.uuid1)
    source = models.CharField(u"来源", max_length=15, default='ios')
    created_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(u"过期时间", default=timezone.now)
    is_del = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.expire_time = timezone.now() + timezone.timedelta(days=30)
        super(AppUsers, self).save(*args, **kwargs)

    def is_authenticated(self):
        return True


class WeixinUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    openid = models.CharField(u'openid', max_length=50)
    unionid = models.CharField(u'uuid', max_length=50, default='')
    skey = models.CharField(max_length=50, default='')
    sid = models.UUIDField(default=uuid.uuid1)
    is_del = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user

    class Meta:
        ordering = ['-pk']
        get_latest_by = "pk"


class AccessToken(models.Model):
    access_token = models.CharField(max_length=600)
    expiration = models.DateTimeField(blank=False)
    source = models.CharField(u"来源", max_length=15, default='wx')

    def save(self, *args, **kwargs):
        if not self.expiration:
            self.expiration = datetime.datetime.now() + datetime.timedelta(minutes=int(100))
        super(AccessToken, self).save(*args, **kwargs)
