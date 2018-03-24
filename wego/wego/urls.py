"""wego URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import tools.signals  # noqa important! not del it

from django.conf.urls import url, include
from rest_framework import routers

from passport.api import WeixinUserViewSet
from data.api import WeRunViewSet
from adminset.api import UsersViewSet, DataDefineViewSet, SummaryPicViewSet, get_pic, get_default_pic

router = routers.DefaultRouter()
router.register(r'passport/wx', WeixinUserViewSet, base_name='passport_wx'),
router.register(r'werun', WeRunViewSet, base_name='werun'),
router.register(r'users', UsersViewSet)
router.register(r'define', DataDefineViewSet)
router.register(r'summary_pic', SummaryPicViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/captcha/', include('captcha.urls')),
    url(r'^api/passport/', include('passport.urls')),
    url(r'^api/get_pic/', get_pic),
    url(r'^api/get_default_pic/', get_default_pic),
]
