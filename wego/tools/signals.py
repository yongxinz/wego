# coding=utf-8

from django.db.models.signals import post_save
from django.dispatch import receiver

from adminset.models import Users
from passport.models import AppUsers


@receiver(post_save, sender=AppUsers)
def create_users(**kwargs):
    created = kwargs['created']
    instance = kwargs['instance']
    if created:
        user = instance.user
        if not Users.objects.filter(user=user).exists():
            Users.objects.create(user=user)
