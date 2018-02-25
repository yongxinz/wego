# coding=utf-8

from django.contrib.auth.models import User
from django.db import models

from adminset.models import Users


class DayData(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    step = models.IntegerField(u"步数", default=0)
    mileage = models.DecimalField(u"距离", default=0, max_digits=25, decimal_places=2, )
    altitude = models.DecimalField(u"海拔", default=0, max_digits=25, decimal_places=2, )
    calorie = models.DecimalField(u"卡路里", default=0, max_digits=25, decimal_places=2, )
    created_time = models.DateField()

    def get_user_info(self):
        obj = Users.objects.get(user=self.user)
        return {'nickname': obj.nickname, 'avatar_url': obj.avatar_url}

    class Meta:
        ordering = ['-id']
