#-*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    (r'^$', 'market.views.index'),
    (r'^parser/$', 'market.views.parser'),
)
