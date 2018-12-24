from django.conf.urls import url
from django.contrib import admin
from  . import views

urlpatterns=[
	url(r'^$', views.dashbord, name="dashbord"),
	url(r'contact', views.contact, name="contact"),
	url(r'blogs', views.blogs ),
	url(r'^blog/(?P<blog_slug>[-_\w]+)$', views.my_blog),
	url(r'airdrops', views.airdrops , name='airdrops' ),
	url(r'^airdrop/(?P<airdrop_slug>[-_\w]+)$', views.airdrop_single),
	url(r'donate', views.donate, name="donate"),
#	url(r'posts', views.posts , name='posts'),
	url(r'upgrade', views.upgrade , name ='upgrade'),
	url(r'shop', views.shoping , name ='shop'),
	url(r'faq', views.faq, name='faq'),
	url(r'events', views.events),
	
	

#	url(r'^edit', views.edit)
]	#(?P<blog_id>\d+)/

