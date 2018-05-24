# coding=utf-8
from datetime import timedelta, datetime

from django.core.management.base import BaseCommand
from django.db.models import Q

from activity.models import ActivityJoin, Activity
from data.models import DayData


class Command(BaseCommand):
    help = 'Finish activity and grant bonuses'

    def handle(self, *args, **options):
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
