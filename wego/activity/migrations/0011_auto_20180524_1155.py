# Generated by Django 2.0 on 2018-05-24 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0010_activityjoin_reward'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityjoin',
            name='reward',
            field=models.FloatField(default=0, verbose_name='获得奖金'),
        ),
    ]
