from django.conf.urls import patterns, url

from taximanager import views

from django.contrib.auth.views import login, logout


urlpatterns = patterns('',
    url(r'^$', views.taximanager, name='taximanager'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^ridelist/$', views.rideList, name='ridelist'),

    url(r'^ridelist/about/$', views.about, name='about'),

    url(r'^ridelist/(?P<ride_id>\d+)/$', views.selectRide, name='selectRide'),
    url(r'^ridelist/(?P<ride_id>\d+)/changeStatus/$', views.changeStatus, name='changeStatus'),



    url(r'^register/$', views.register, name='register'),


#test url
    url(r'^test1/$', views.Test1.as_view(), name='test1'),
    url(r'^test2/$', views.Test2, name='test2'),

    url(r'^test3/$', views.test3, name='test3'),


    url(r'^testPostForm/$', views.testPostForm, name='testPostForm'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^send/$', views.send, name='send'),


    url(r'^test_bootstrap/$', views.test_bootstrap, name='test_bootstrap'),
    url(r'^bootstrap/$', views.bootstrap, name='bootstrap'),
    url(r'^table/$', views.table, name='table'),
    url(r'^newride/$', views.newRide, name='newRide'),
)