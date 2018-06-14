#!/usr/bin/env python
# coding=utf-8

from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'wego',
    }
}

INSTALLED_APPS += [
    'rest_framework',
]

WEIXIN = {
    'url': 'https://api.weixin.qq.com',
    'id': 'wx2d7e3590b4d63791',
    'key': 'a4be29fc6e97553bc9ee4492fecfc9da',
    'mch_id': '1505152531',
    'mch_key': 'C118FF0D80378CE3BFC5F576C09A2179'
}
