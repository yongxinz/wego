# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers

from adminset.models import Users


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        exclude = ('user', )
