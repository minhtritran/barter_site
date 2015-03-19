from django.conf.urls import patterns, url

from barter import views

urlpatterns = patterns(
    '',
    url('^register/', views.register, name='register'),
    url(r'^$', views.home, name='home'),
    url(r'^favor/$', views.FavorList.as_view(), name='favor_list'),
    url(r'^favor/(?P<pk>\d+)/$', views.FavorDetail.as_view(), name='favor_detail'),
    url(r'^user/(?P<pk>\d+)/$', views.UserDetail.as_view(), name='user_detail')
)