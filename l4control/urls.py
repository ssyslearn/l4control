from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'l4control.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('l4ui.urls')),
    #url(r'^accounts/', include('django.contrib.auth.urls'))
    # url(r'^accounts/', include('django.contrib.auth.urls')),
    #url(r'^logout/$', auth_views.logout, {'next_page' : '/'}),
    #url(r'^login/$', auth_views.login,  {'template_name':'registration/login.html'}),
    url(r'^login/$', django.contrib.auth.views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', django.contrib.auth.views.logout, {'next_page': '/'}, name='logout'),
]
