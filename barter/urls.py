from django.conf.urls import patterns, url

from barter import views
from barter.views import custom_login

urlpatterns = patterns(
    '',
    url('^login/', custom_login, name="login"),
    url('^register/', views.register, name='register'),
    url(r'^$', views.home, name='home'),
    url(r'^favors/$', views.FavorList.as_view(), name='favor_list'),
    url(r'^favors/tag/(?P<slug>[-\w\d]+)/$', views.FavorList.as_view(), name='favor_list_tagged'),
    url(r'^favors/(?P<pk>\d+)/$', views.FavorDetail.as_view(), name='favor_detail'),
    url(r'^favors/create/$', views.FavorCreate.as_view(), name='favor_create'),
    url(r'^favors/create/finish$', views.create_favor, name='create_favor'),
    url(r'^tags/$', views.TagList.as_view(), name='tag_list'),
    url(r'^users/$', views.UserList.as_view(), name='user_list'),
    url(r'^users/(?P<pk>\d+)/$', views.UserDetail.as_view(), name='user_detail')
)
