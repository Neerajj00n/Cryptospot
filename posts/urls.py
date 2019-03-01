from django.conf.urls import url
from django.contrib import admin
from posts import views
from django.contrib.auth.models import User 
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns=[ 
	url(r'posts', views.post , name='posts'),
	url(r'^(?P<username>[\w-]+)$', views.profile , name='profile'),
	url(r'register', views.register,),
	url(r'login', views.auth_login, name='auth_login'),
	url(r'^edit/(?P<username>[\w-]+)$', views.editProfile, name='profile-edit'),

#    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
#    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^post/new/', PostCreate.as_view(), name='post-create'),
    url(r'^post/(?P<pk>\d+)/edit/', PostEdit.as_view(), name='post-edit'),
    url(r'^post/(?P<pk>\d+)/delete/', PostDelete.as_view(), name='post-delete'),
	url(r'^follow/(?P<pk>\d+)/$', views.follow, name='follow'),
	url(r'^unfollow/(?P<pk>\d+)/$', views.unfollow, name='unfollow'),
	url(r'^(?P<username>[\w-]+)/logout', views.logout_view, name="logout_view"),
	url(r'^search/$', views.search, name='search'),
	url(r'^post/(?P<pk>\d+)/upvote', views.upvote, name='upvote'),
	url(r'^post/(?P<pk>\d+)/downvote', views.downvote, name='downvote'),

#password resat

	
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    	auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]

	