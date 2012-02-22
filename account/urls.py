#-*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from django.views.generic.create_update import create_object

from account.forms import UserCreateForm

urlpatterns = patterns('',
    (r'^$', 'account.views.account'),
    (r'^login/$', 'account.views.login'),
    (r'^register/$', 'account.views.register'),
    (r'^logout/$', 'account.views.logout'),
)
