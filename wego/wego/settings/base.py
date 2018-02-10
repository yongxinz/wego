#!/usr/bin/env python
# coding=utf-8

from .settings import *
from os.path import join, abspath, dirname

# make root path
here = lambda *x: join(abspath(dirname(__file__)), *x)
PROJECT_ROOT = here("..", "..")
root = lambda *x: join(abspath(PROJECT_ROOT), *x)

DEBUG = False

TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-hans'

ALLOWED_HOSTS = [
    '127.0.0.1',
]

INSTALLED_APPS += [
    'captcha',
    'passport',
    'adminset',
    'activity',
    'data'
]

SMS = {
    "url": "http://222.73.117.156",
    "uid": "youmutou",
    "key": "Tch778899"
}

WEIXIN = {
    'url': 'https://api.weixin.qq.com',
    'id': 'wx2d7e3590b4d63791',
    'key': 'a4be29fc6e97553bc9ee4492fecfc9da',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('tools.auth.YMAuthentication',),
    'DEFAULT_PAGINATION_CLASS': 'tools.rest_helper.YMPagination',
}
