# coding=utf-8

from django.utils import timezone
from rest_framework import authentication, exceptions
from rest_framework.pagination import PageNumberPagination

from passport.models import AppUsers


class YMAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        hash_key = request.META.get('HTTP_AUTHORIZATION', '123abc')
        try:
            user = AppUsers.objects.get(hashKey=hash_key, is_del=False, expire_time__gt=timezone.now())
        except:
            raise exceptions.AuthenticationFailed({'status': False, 'msg': u'用户验证失败，请重新登录'})

        return user.user, None


class YMPagination(PageNumberPagination):
    page_size = 16
    page_size_query_param = 'size'
    max_page_size = 1000


class YMMixin(object):
    def get_queryset(self):
        queryset = self.queryset.filter(company=self.request.auth.company)
        return queryset

    def perform_create(self, serializer):
        update_dict = {}
        company = self.request.auth.company
        update_dict['company'] = company

        if 'operator' in serializer.fields:
            operator = self.request.user.username
            update_dict['operator'] = operator
        serializer.save(**update_dict)

    def perform_destroy(self, instance):
        instance.is_del = True
        instance.save()
