from django.conf.urls import patterns, url

from barter import views

urlpatterns = patterns(
    '',
    url('^register/', views.register, name='register'),
    url(r'^$', views.home, name='home'),
    url(r'^user/$', views.user, name='user')
)