# coding: utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^create/$', views.image_create, name='image_create'),
    url(r'^detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.detail, name='detail'),
    url(r'^like/$', views.image_like, name='like'),
    url(r'^$', views.image_list, name='list'),
    url(r'^detail_list/$', views.detail_list, name='detail_list'),
]
