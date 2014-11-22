from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('taximanager.urls', namespace="taximanager")),
    url(r'^login/$', login),
    url(r'^admin/', include(admin.site.urls)),
)
