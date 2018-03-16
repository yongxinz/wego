# coding=utf-8

from rest_framework.pagination import PageNumberPagination


class YMPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'size'
    max_page_size = 1000


class YMMixin(object):
    def get_queryset(self):
        queryset = self.queryset
        return queryset

    def perform_create(self, serializer):
        update_dict = {}

        serializer.save(**update_dict)

    def perform_destroy(self, instance):
        instance.status = 'DEL'
        instance.save()
