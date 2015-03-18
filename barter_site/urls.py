from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^', include('barter.urls', namespace='barter')),
    url(r'^admin/', include(admin.site.urls)),
)
