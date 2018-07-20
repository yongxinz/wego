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
    '127.0.0.1', '192.168.8.110', 'wego.lvzhouhuwai.com', 'deal.lvzhouhuwai.com'
]

INSTALLED_APPS += [
    'captcha',
    'passport',
    'adminset',
    'activity',
    'data'
]

TO_KCAL = 40
TO_MILE = 0.7

CONTENT = '• 奖金池为参与活动者支付的鼓励金之和 \r\n \
• 在活动活动时间内完成挑战的“参战者”共同评分奖金池奖金 \r\n \
• 如都未完成挑战，则鼓励金归入下一次活动 \r\n \
• 挑战成后，奖金将在活动结束后第二天上午10:00发放到微信零钱 \r\n \
• 数据统计时间：活动开始日期 00:00 - 活动结束日期 24:00 \r\n \
• 数据更新时机：以活动开始到结束后第二天上午9:00前，最后一次进入小程序更新的为准 \r\n \
• 关注“绿洲户外”公众号，每天23:00点，推送步数更新提醒'

WHITE_LIST = ['18610011929', '18801089166', '13910843366']

SMS = {
    "url": "http://222.73.117.156",
    "uid": "beijinaimei",
    "key": "Beijinai8211"
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('tools.auth.YMAuthentication',),
    'DEFAULT_PAGINATION_CLASS': 'tools.rest_helper.YMPagination',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}
