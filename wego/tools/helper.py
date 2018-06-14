# coding=utf-8

import json
import datetime
import re
import random
import requests
import hashlib
import xml.etree.ElementTree as ET

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class Helper(object):
    @classmethod
    def get_safe_now(self):
        try:
            from django.utils.timezone import utc
            if settings.USE_TZ:
                return datetime.datetime.utcnow().replace(tzinfo=utc)
        except:
            pass

        return datetime.datetime.now()

    @classmethod
    def mk_random(self, num=8, ram_type='str'):
        ram_int = '1234567890'
        ram_str = 'abcdefghigklmnopqrstuvwxyz1234567890'

        if ram_type != 'str':
            ram_str = ram_int

        return "".join(random.sample(ram_str, num))

    @classmethod
    def password_format_check(self, password):
        result = {"status": True}
        # 至少8位
        if len(password) < 8:
            result.update({"status": False, 'msg': "密码过于简单，密码至少8位"})
        # 至少一个数字
        if not re.match(r'.*[0-9]+', password):
            result.update({"status": False, 'msg': "密码过于简单，至少包括一个数字"})
        # 至少一个小写字母
        if not re.match(r'.*[a-zA-Z]+', password):
            result.update({"status": False, 'msg': "密码过于简单，至少包括一个字母"})

        return result

    @classmethod
    def mobile_format_check(self, mobile):
        result = {"status": True}
        # 至少11位
        if len(mobile) != 11:
            result.update({"status": False, 'msg': "请填写11位手机号码"})
        # 全部数字
        if not re.match(r'^1[0-9]{10}', mobile):
            result.update({"status": False, 'msg': "手机格式不对，请填写11位手机号码"})

        return result


class Json2obj(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)


class Dict2obj(object):
    def __init__(self, d):
        self.__dict__ = d

    def __str__(self):
        return str(self.__dict__)


def random_digit_challenge():
    ret = u''
    for i in range(4):
        ret += str(random.randint(0, 9))
    return ret, ret


class YMapi(object):
    # YMapi.get('adp', 'erp').json()

    @classmethod
    def get(self, api='url', service='erp', uri='', params=None):
        host = settings.API_SRV.get(service).get('host')
        api = settings.API_SRV.get(service).get('api').get(api)
        auth = settings.API_SRV.get(service).get('authorization')
        r = requests.get(url=host + api + uri, headers={'AUTHORIZATION': auth}, params=params)
        return r

    @classmethod
    def post(self, api='url', service='erp', params=None, data=None, pk=''):
        host = settings.API_SRV.get(service).get('host')
        api = settings.API_SRV.get(service).get('api').get(api)
        auth = settings.API_SRV.get(service).get('authorization')
        pk = (pk + '/') if pk else ''
        r = requests.post(url=host + api + pk, headers={'AUTHORIZATION': auth}, params=params, json=data)
        return r

    @classmethod
    def put(self, api='url', service='erp', params=None, data=None, pk=''):
        host = settings.API_SRV.get(service).get('host')
        api = settings.API_SRV.get(service).get('api').get(api)
        auth = settings.API_SRV.get(service).get('authorization')
        pk = (pk + '/') if pk else ''
        r = requests.put(url=host + api + pk, headers={'AUTHORIZATION': auth}, params=params, json=data)
        return r

    @classmethod
    def patch(self, api='url', service='erp', params=None, data=None, pk=''):
        host = settings.API_SRV.get(service).get('host')
        api = settings.API_SRV.get(service).get('api').get(api)
        auth = settings.API_SRV.get(service).get('authorization')
        pk = (pk + '/') if pk else ''
        r = requests.patch(url=host + api + pk, headers={'AUTHORIZATION': auth}, params=params, json=data)
        return r

    @classmethod
    def delete(self, api='url', service='erp', params=None, pk=''):
        host = settings.API_SRV.get(service).get('host')
        api = settings.API_SRV.get(service).get('api').get(api)
        auth = settings.API_SRV.get(service).get('authorization')
        pk = (pk + '/') if pk else ''
        r = requests.delete(url=host + api + pk, headers={'AUTHORIZATION': auth}, params=params)
        return r


def paginator(data, paginate_num=10, page_num=1):
    """
    分页
    """
    paginator = Paginator(data, paginate_num)
    try:
        contacts = paginator.page(page_num)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return contacts


def dict_to_xml(dict_data):
    """
    dict to xml
    :param dict_data:
    :return:
    """

    xml = ["<xml>"]
    for k, v in dict_data.items():
        xml.append("<{0}>{1}</{0}>".format(k, v))
    xml.append("</xml>")

    return "".join(xml)


def xml_to_dict(xml_data):
    """
    xml to dict
    :param xml_data:
    :return:
    """

    xml_dict = {}
    root = ET.fromstring(xml_data)
    for child in root:
        xml_dict[child.tag] = child.text

    return xml_dict


def generate_sign(data, mch_key):
    stringA = '&'.join(["{0}={1}".format(k, data.get(k)) for k in sorted(data)])
    stringSignTemp = '{0}&key={1}'.format(stringA, mch_key)
    sign = hashlib.md5(stringSignTemp.encode('utf-8')).hexdigest()

    return sign.upper()
