# Generated by Django 2.0 on 2018-05-23 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0009_auto_20180511_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityjoin',
            name='reward',
            field=models.IntegerField(default=0, verbose_name='获得奖金'),
        ),
    ]
