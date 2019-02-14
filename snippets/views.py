# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.test import APITestCase, APIClient
from posts.models import Signels
from . serializers import SignelsSerializer
# Create your views here.


class signelsList(APIView):
	"""docstring for Signelslist"""
	def get(self, request, username):
		users = User.objects.get(username=username)
		Signel = Signels.objects.filter(author=users)
		serializer = SignelsSerializer(Signel, many=True)
		return Response(serializer.data)		

	def post(self):
		pass
		