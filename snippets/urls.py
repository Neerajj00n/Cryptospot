from django.conf.urls import url, include
from django.contrib import admin
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	url(r'^api/(?P<username>[\w-]+)$',views.signelsList.as_view(), name='signals'),
]

urlpatterns = format_suffix_patterns(urlpatterns)