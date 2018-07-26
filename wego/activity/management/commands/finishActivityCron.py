# coding=utf-8
from datetime import timedelta, datetime
import time
import uuid
import requests

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.conf import settings

from activity.models import ActivityJoin, Activity
from data.models import DayData
from tools.helper import Dict2obj, dict_to_xml, generate_sign


class Command(BaseCommand):
    help = 'Finish activity and grant bonuses'

    def handle(self, *args, **options):
        # conf = Dict2obj(settings.WEIXIN)
        # data = {
        #     'mch_appid': conf.id,
        #     'mchid': conf.mch_id,
        #     'nonce_str': str(uuid.uuid4()).replace('-', ''),
        #     'desc': 'WeGo活动奖励'.encode('utf-8'),
        #     'openid': 'oujiG5BWZqneBMm3qUQwGgFklhVo',
        #     'partner_trade_no': str(int(time.time())),
        #     'amount': 1,
        #     'spbill_create_ip': '127.0.0.1',
        #     'check_name': 'NO_CHECK'
        # }
        # sign = generate_sign(data, conf.mch_key)
        # data['sign'] = sign
        # xml_data = dict_to_xml(data)
        # response = requests.post('https://api.mch.weixin.qq.com/mmpaymkttransfers/promotion/transfers',
        #                          data=xml_data, headers={'Content-type': 'text/xml'},
        #                          cert=('/Users/zyx/lvzhou/cert/apiclient_cert.pem', '/Users/zyx/lvzhou/cert/apiclient_key.pem'))
        # print(response.text)

        yesterday = datetime.today() + timedelta(-1)
        yesterday_format = yesterday.strftime('%Y-%m-%d')

        user_success = []
        obj = Activity.objects.filter(type='D')
        for item in obj:
            obj_ = ActivityJoin.objects.filter(activity=item.id, status='JOI', end_time=yesterday_format)
            for item_ in obj_:
                data = DayData.objects.get(user=item_.user, created_time=yesterday_format)
                if data.step >= item.target_step:
                    user_success.append(item_.user)

            count = obj_.count()
            reward = item.reward * count

            if len(user_success) > 0:
                reward_avg = reward / len(user_success)
            else:
                reward_avg = 0
            ActivityJoin.objects.filter(activity=item.id, status='JOI', end_time=yesterday_format, user__in=user_success).update(reward=reward_avg)

        ActivityJoin.objects.filter((Q(status='JOI') | Q(status='OBS')), end_time=yesterday_format).update(status='FIN')
