# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect 
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.models import User 
from .models import Configration
from blog.models import *
from .models import Profile
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from dashboard.models import * 
import requests
from django.core.mail import send_mail, BadHeaderError , EmailMessage 
from notifications.signals import notify
# Create your views here.

conf =  Configration.objects.all()
user = User.objects.all()






def contact(request):
	crypt = Dashconf.objects.get()
	con = "Contact us"
	if request.method == 'POST':
		firstname = request.POST['fname']
		lastname = request.POST['lname']
		email = request.POST['email']
		subject = request.POST['subject']
		message = request.POST['message']
		name = firstname +' '+lastname
		msg = name +" "+ message



	 	try:
	 		mail = EmailMessage(subject, msg, email, ['neerajjoon0@gmail.com'], reply_to=[email])
	 		mail.send()
	 	

	 		return redirect('dashbord')

	 	except BadHeaderError:
	 		print email
	 		return HttpResponse('Invalid header found.')


	return render(request, 'dashbord/contact.html', {"crypto": crypt , "header": con })




	return render(request, 'login.html', {})

def dashbord(request):
	crypt = Dashconf.objects.get()
	signel = Signels.objects.all()
	listing = Coin_listings.objects.all()
	dash = "Dashboard"

#	noti = notify.send(user, recipient=user, verb='you reached level 10')


	return render(request, "dashbord/dashbord.html", {"crypto": crypt , "signels" : reversed(signel), "listing": reversed(listing), "header": dash }) #'order': order }) 


def blogs(request):
	crypt = Dashconf.objects.get()
	blogs = Blog.objects.all()
	return render(request, "dashbord/blogs.html", {"crypto": crypt, "blog": blogs})

def my_blog(request, blog_slug):
	title1=''
	try:
		blog = Blog.objects.get(slug=blog_slug)
		title1=k.title
	except:
		title1='blog not exist'


	return render(request, "dashbord/blog_single.html", {'blog': blog})


def listing(request):
	crypt = Dashconf.objects.get()
	airdrop = Airdrop.objects.all()
	air = "Airdrops"

	return render(request, "dashbord/table.html", {"crypto": crypt , "airdrop": reversed(airdrop), "header": air})


def shoping(request):
	crypt = Dashconf.objects.get()
	shop  = Shop.objects.all()
	

	sop = "Shop"

	return render(request, "dashbord/shop.html", {"crypto": crypt , "shop": shop , 'header': sop})


def posts(request):
	return render(request, "dashbord/notifications.html", {})


def faq(request):
	crypt = Dashconf.objects.get()
	return render(request, "dashbord/FAQ.html", {"crypto": crypt})


def upgrade(request):
	return render(request, "dashbord/upgrade.html", {})

def donate(request):
	return render(request, "dashbord/donate.html", {})






