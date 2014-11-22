from django.conf.urls import patterns, url
from taximanager import views

urlpatterns = patterns('',
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^ridelist/$', views.ride_list, name='ridelist'),
    url(r'^drivers/$', views.drivers, name='drivers'),
    url(r'^ridelist/(?P<ride_id>\d+)/$', views.select_ride, name='selectRide'),
    url(r'^ridelist/(?P<ride_id>\d+)/change$', views.change_ride, name='changeRide'),
    url(r'^ridelist/(?P<ride_id>\d+)/changeStatus/$', views.change_status, name='changeStatus'),
    url(r'^(?P<driver_id>\d+)/changeStatusDriver/$', views.change_status_driver, name='changeStatusDriver'),
    url(r'^newride/$', views.new_ride, name='newRide'),
)