import django_filters

from .models import ActivityJoin


class ActivityJoinFilter(django_filters.rest_framework.FilterSet):
    start_time = django_filters.IsoDateTimeFilter(name="start_time", lookup_expr='gte')
    end_time = django_filters.IsoDateTimeFilter(name="end_time", lookup_expr='lte')

    class Meta:
        model = ActivityJoin
        exclude = ['created_time', ]
