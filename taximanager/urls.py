from django.conf.urls import patterns, url

from taximanager import views

from django.contrib.auth.views import login, logout


urlpatterns = patterns('',
    url(r'^$', views.taximanager, name='taximanager'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^ridelist/$', views.rideList, name='ridelist'),


    url(r'^drivers/$', views.drivers, name='drivers'),


    url(r'^ridelist/(?P<ride_id>\d+)/$', views.selectRide, name='selectRide'),

    url(r'^ridelist/(?P<ride_id>\d+)/change$', views.changeRide, name='changeRide'),


    url(r'^ridelist/(?P<ride_id>\d+)/changeStatus/$', views.changeStatus, name='changeStatus'),

    url(r'^(?P<driver_id>\d+)/changeStatusDriver/$', views.changeStatusDriver, name='changeStatusDriver'),






    url(r'^newride/$', views.newRide, name='newRide'),
)