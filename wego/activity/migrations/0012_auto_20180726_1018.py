# Generated by Django 2.0 on 2018-07-26 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0011_auto_20180524_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityjoin',
            name='end_time',
            field=models.DateField(verbose_name='结束时间'),
        ),
        migrations.AlterField(
            model_name='activityjoin',
            name='start_time',
            field=models.DateField(verbose_name='开始时间'),
        ),
    ]