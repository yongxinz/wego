# Generated by Django 2.0 on 2018-02-06 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passport', '0002_auto_20180202_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='weixinusers',
            name='is_del',
            field=models.BooleanField(default=False),
        ),
    ]
