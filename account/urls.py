from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.views.generic.create_update import create_object

urlpatterns = patterns('',
    (r'^register/$', 'account.views.register'),
    #url(r'^register/$', create_object, {
    ##                                   'form_class': UserCreateForm, 
     ##                                  'template_name': 'account/create.html',
       ##                                'post_save_redirect': '/account/autologin'
        ##                               }, name='account.views.register'),
)
