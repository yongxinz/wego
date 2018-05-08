import django_filters

from .models import ActivityJoin


class ActivityJoinFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = ActivityJoin
        exclude = ['created_time', ]
