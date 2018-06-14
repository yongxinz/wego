# coding=utf-8
from rest_framework import authentication, exceptions

from adminset.models import Users
from passport.models import AppUsers, WeixinUsers
from tools.helper import Dict2obj


class YMAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        hash_key = request.META.get('HTTP_AUTHORIZATION', '123abc')
        try:
            user = AppUsers.objects.get(hash_key=hash_key, is_del=False)
            obj = Users.objects.get(user=user.user)
            obj_ = WeixinUsers.objects.get(user=user.user)
        except:
            raise exceptions.AuthenticationFailed({
                'status': False,
                'status_code': 403010,
            })
        return user.user, Dict2obj({
            'target': obj.target, 'openid': obj_.openid
        })
