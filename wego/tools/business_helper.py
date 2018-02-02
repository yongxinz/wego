# coding=utf-8
from __future__ import print_function
import uuid
import datetime

from django.conf import settings
from django.db.models import F
from django.contrib.auth.models import User
from captcha.models import CaptchaStore

from tools.sms import Sms
from tools.helper import Helper
from passport.models import CodeDB, AppUsers


def captcha_check(imgcode, imgkey):
    check_status = CaptchaStore.objects.filter(
        hashkey=imgkey,
        response=imgcode.lower(),
        expiration__gt=Helper.get_safe_now()
    ).exists()

    return check_status


def sms_check(mobile, smscode, hashkey=None):
    start_date = Helper.get_safe_now() - datetime.timedelta(seconds=300)
    has_sms = CodeDB.objects.filter(
        mobile=mobile, limit_times__lte=5, created__gte=start_date
    )
    has_sms.update(limit_times=F('limit_times') + 1)
    if hashkey:
        return has_sms.filter(sms_code=smscode, hashkey=hashkey).exists()

    return has_sms.filter(sms_code=smscode).exists()


def send_sms_by_key(mobile, imgkey=''):
    start_date = Helper.get_safe_now() - datetime.timedelta(seconds=60)
    result = {"status": False}

    if CodeDB.objects.filter(mobile=mobile, created__gte=start_date).exists():
        result.update({"msg": "60秒内只能发送一次哦！请稍后重试！"})
    else:
        random_int = Helper.mk_random(num=4, ram_type='int')
        msg = "验证码: %s" % random_int
        if settings.DEBUG:
            CodeDB.objects.create(mobile=mobile, sms_code=random_int, hashkey=imgkey)
            result.update({"status": True, "msg": "DEBUG模式,短信验证码不发送到手机 -> " + msg})
        else:
            r_text = Sms.send_sms(text=msg, mobile=mobile)
            status = r_text.split(',')
            if status[1] == '0':
                CodeDB.objects.create(mobile=mobile, sms_code=random_int, hashkey=imgkey)
                result.update({"status": True, "msg": "短信验证码已发送，请查看手机!"})
            else:
                result.update({"msg": "短信验证码发送失败，请稍后重试！"})

    return result


def get_or_create_user(mobile, password=None):
    if User.objects.filter(username=mobile).exists():
        user = User.objects.get(username=mobile)
        if password:
            user.set_password(password)
            user.save()
    else:
        if not password:
            password = uuid.uuid4().hex
        user = User.objects.create_user(mobile, 'default@youmutou.com', password)
        # todo 新用户同时新建公司，并绑定
        Company.objects.create(user=[user.pk])

    return user


def reset_pawd(mobile, password):
    result = {"status": False}

    if User.objects.filter(username=mobile).exists():
        user = User.objects.get(username=mobile)
        user.set_password(password)
        user.save()

        obj, is_new = AppUsers.objects.get_or_create(user=user, source='mall', is_del=False)
        if not is_new:
            obj.hashKey = uuid.uuid1()
            obj.save()

        result.update({"status": True, "msg": "密码重置成功!", 'userhashid': obj.hashKey})
    else:
        result.update({"status": False, "msg": "账户不存在,请输入正确的手机号码!"})

    return result
