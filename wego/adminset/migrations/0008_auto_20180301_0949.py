# Generated by Django 2.0 on 2018-03-01 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminset', '0007_datadefine_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datadefine',
            name='reference_value',
            field=models.FloatField(default=0, verbose_name='参考物数值'),
        ),
        migrations.AlterField(
            model_name='datadefine',
            name='type',
            field=models.CharField(choices=[('M', '里程(km)'), ('S', '步数'), ('C', '卡路里')], default='K', max_length=1, verbose_name='数据类型'),
        ),
    ]
