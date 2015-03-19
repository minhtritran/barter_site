from django.conf.urls import patterns, include, url
from django.contrib import admin
from barter.views import custom_login

urlpatterns = patterns(
    '',
    url('^login/', custom_login, name="login"),
    url('^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^', include('barter.urls', namespace='barter')),
    url(r'^admin/', include(admin.site.urls)),
)
