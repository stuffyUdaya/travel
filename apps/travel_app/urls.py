from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^success$', views.success),
    url(r'^addtravelplan/(?P<id>\d+)$', views.addtravelplan),
    url(r'^addtrip/(?P<id>\d+)$', views.addtrip),
    url(r'^viewtrip/(?P<id>\d+)$', views.viewtrip),
    url(r'^join/(?P<id>\d+)/(?P<uid>\d+)$', views.jointrip),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
]
