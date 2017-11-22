#-*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.create_l4, name='create_l4'),
    url(r'^create$', views.create_l4, name='create_l4'),
    url(r'^modify$', views.modify_l4, name='modify_l4'),
    url(r'^search_l4check', views.search_l4check, name='search_l4check'),
    url(r'^verify_vip', views.verify_vip, name='verify_vip'),
    url(r'^l4map$', views.l4map, name='l4map'),
    url(r'^test$', views.test, name='test')
]
