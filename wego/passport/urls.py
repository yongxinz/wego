from django.conf.urls import url
from .api import login, captcha_refresh, join, info


urlpatterns = [
    url(r'^captcha/refresh/$', captcha_refresh, name='passport_login'),
    url(r'^login/$', login, name='passport_login'),
    url(r'^join/$', join, name='passport_join'),
    url(r'^info/$', info, name='passport_info'),
]