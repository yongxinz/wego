# Generated by Django 2.0 on 2018-04-18 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0003_auto_20180418_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activityjoin',
            name='is_creater',
        ),
        migrations.RemoveField(
            model_name='activityjoin',
            name='is_observe',
        ),
        migrations.AlterField(
            model_name='activity',
            name='end_time',
            field=models.DateField(verbose_name='结束时间'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='start_time',
            field=models.DateField(verbose_name='开始时间'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='status',
            field=models.CharField(choices=[('CIM', '已提交'), ('ONL', '已上线'), ('FIN', '已结束'), ('DEL', '已删除'), ('OBS', '已观战'), ('JOI', '已参加')], default='ONL', max_length=5, verbose_name='活动状态'),
        ),
        migrations.AlterField(
            model_name='activityjoin',
            name='status',
            field=models.CharField(choices=[('CIM', '已提交'), ('ONL', '已上线'), ('FIN', '已结束'), ('DEL', '已删除'), ('OBS', '已观战'), ('JOI', '已参加')], default='JOI', max_length=5, verbose_name='活动状态'),
        ),
    ]
