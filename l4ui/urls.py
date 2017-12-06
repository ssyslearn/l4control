#-*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.create_l4, name='create_l4'),
    url(r'^create$', views.create_l4, name='create_l4'),
    url(r'^modify$', views.modify_l4, name='modify_l4'),
    url(r'^search_l4check', views.search_l4check, name='search_l4check'),
    url(r'^verify_vip', views.verify_vip, name='verify_vip'),
    url(r'^search_matched_dev', views.search_matched_dev, name='search_matched_dev'),
    url(r'^search_usable_vip', views.search_usable_vip, name='search_usable_vip'),
    url(r'^test$', views.test, name='test')
]
