from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url('^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^', include('barter.urls', namespace='barter')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^messages/', include('postman.urls')),
    url(r'^favors/search/', include('haystack.urls')),
)
