# coding=utf-8
from rest_framework import authentication, exceptions

from passport.models import AppUsers
from tools.helper import Dict2obj


class YMAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        hash_key = request.META.get('HTTP_AUTHORIZATION', '123abc')
        try:
            user = AppUsers.objects.get(hash_key=hash_key, is_del=False)
        except:
            raise exceptions.AuthenticationFailed({
                'status': False,
                'status_code': 403010,
            })
        return user.user, Dict2obj({
            'appuser': user,
        })
