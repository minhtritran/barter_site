from django.conf.urls import patterns, url
from barter import views
from barter.views import custom_login
from django.contrib.auth.decorators import login_required
# from dajaxice.core import dajaxice_config
# from dajaxice.core.Dajaxice import dajaxice_autodiscover
# dajaxice_autodiscover()


urlpatterns = patterns(
    '',
    # url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url('^login/', custom_login, name="login"),
    url('^register/', views.register, name='register'),
    url(r'^$', views.FavorList.as_view()),
    url(r'^home/$', views.home, name='home'),
    url(r'^favors/$', views.FavorList.as_view(), name='favor_list'),
    url(r'^favors/tag/(?P<slug>[-\w\d]+)/$', views.FavorList.as_view(), name='favor_list_tagged'),
    url(r'^favors/user/(?P<user_pk>\d+)/$', views.FavorList.as_view(), name='favor_list_user'),
    url(r'^favors/(?P<pk>\d+)/$', views.FavorDetail.as_view(), name='favor_detail'),
    url(r'^favors/(?P<pk>\d+)/offers/(?P<trader_pk>\d+)$', views.create_offer, name='create_offer'),
    url(r'^favors/(?P<pk>\d+)/offers/(?P<trader_pk>\d+)/accept/$', views.accept_offer, name='accept_offer'),
    url(r'^favors/create/$', login_required(views.FavorCreate.as_view()), name='favor_create'),
    url(r'^favors/create/finish$', views.create_favor, name='create_favor'),
    url(r'^tags/$', views.TagList.as_view(), name='tag_list'),
    url(r'^users/$', views.UserList.as_view(), name='user_list'),
    url(r'^users/(?P<pk>\d+)/$', views.UserDetail.as_view(), name='user_detail'),
    url(r'^users/(?P<pk>\d+)/edit$', views.user_edit, name='user_edit'),
    url(r'^users/(?P<pk>\d+)/edit/finish$', views.user_edit, name='user_edit_finish'),
    url(r'^users/(?P<pk>\d+)/feedback/$', views.create_feedback, name='feedback'),
)
