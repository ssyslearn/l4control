from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.create_l4, name='create_l4'),
    url(r'^test$', views.test, name='test'),
]
