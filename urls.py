from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.views.generic.create_update import create_object

from account.forms import UserCreateForm

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    (r'^$', direct_to_template, {'template': 'pages/index.html', 'extra_context': {'PAGE_NAME': 'index'}}),
    (r'^contact/$', direct_to_template, {'template': 'pages/contact.html', 'extra_context': {'PAGE_NAME': 'contact'}}),
    url(r'^account/', include('account.urls')),
    url(r'^market/', include('market.urls')),
    url(r'^investment/', include('investment.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
