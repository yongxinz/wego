# Generated by Django 2.0 on 2018-02-26 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminset', '0005_auto_20180225_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataDefine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('K', '里程'), ('S', '步数')], default='K', max_length=1, verbose_name='数据类型')),
                ('min_value', models.IntegerField(default=0, verbose_name='数据分级小')),
                ('max_value', models.IntegerField(default=0, verbose_name='数据分级大')),
                ('reference', models.CharField(default='', max_length=10, verbose_name='参考物')),
                ('reference_value', models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='参考物数值')),
                ('summary', models.CharField(default='', max_length=100, verbose_name='分享文案')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
