#-*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    (r'^wallet/$', 'investment.views.wallet'),
    (r'^charge/$', 'investment.views.charge'),
    (r'^create/$', 'investment.views.create'),
)