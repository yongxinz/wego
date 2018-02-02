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
    'activity'
]

SMS = {
    "url": "http://222.73.117.156",
    "uid": "youmutou",
    "key": "Tch778899"
}

WEIXIN = {
    'url': 'https://api.weixin.qq.com',
    'id': 'wx6e33d6ee4b1d2251',
    'key': '091c11eceedc2d8bcf8736c086e43359',
}
