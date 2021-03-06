# Generated by Django 2.0 on 2018-02-01 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_key', models.UUIDField(default=uuid.uuid1, verbose_name='')),
                ('source', models.CharField(default='ios', max_length=15, verbose_name='来源')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('expire_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='过期时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CodeDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=15)),
                ('sms_code', models.CharField(max_length=10)),
                ('hash_key', models.CharField(default='989997b9ea3ef632d1cf796f5e02f36dd4d31986', max_length=40)),
                ('limit_times', models.IntegerField(default=0)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WeixinUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(max_length=50, verbose_name='openid')),
                ('unionid', models.CharField(default='', max_length=50, verbose_name='uuid')),
                ('skey', models.CharField(default='', max_length=50)),
                ('sid', models.UUIDField(default=uuid.uuid1)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-pk'],
                'get_latest_by': 'pk',
            },
        ),
    ]
