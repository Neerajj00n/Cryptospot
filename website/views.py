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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from notifications.signals import notify
import requests
import json

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


	uri = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY="

	api = "a502c1f3-72e0-407a-aa7e-ece644776306"

	url = uri + api

	raw_data = requests.get(url).json()

	data = raw_data['data']

	for i in signel:
		if i.signal_id == 0:
			coin = i.symbol.upper()
			for sym in data:
				if coin in sym['symbol']:
					ids = sym['id']
					i.signal_id = ids
					i.save()
				else: 
					pass
		else:
			pass

	for s in listing:
		if s.coin_id == 0:
			lst = s.cymbol.upper()
			for sig in data:
				if lst in sig['symbol']:
					ide = sig['id']
					s.coin_id = ide
					s.save()
				else: 
					pass
		else:
			pass


	return render(request, "dashbord/dashbord.html", {"crypto": crypt , "signels" : reversed(signel), "listing": reversed(listing), "header": dash }) #'order': order }) 


def blogs(request):
	crypt = Dashconf.objects.get()
	contact_list = Blog.objects.all()

	paginator = Paginator(contact_list, 2) # Show 25 contacts per page

	page = request.GET.get('page')

	try:
    		blogs = paginator.page(page)
	except PageNotAnInteger:
        	# If page is not an integer, deliver first page.
    		blogs = paginator.page(1)
	except EmptyPage:
        	# If page is out of range (e.g. 9999), deliver last page of results.
    		blogs = paginator.page(paginator.num_pages)

	
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

def events(request):
	crypt = Dashconf.objects.get()
	event = "Coin events"

	if request.method == "POST":
		srch = request.POST["search"]
		search = srch.upper()
		 
		urls = "https://api.coinmarketcal.com/v1/coins?access_token=ZmEyMWVmNWM4ZTgzMDAwNjI5NmRkZGYzM2NlMGE5YWI3YzkzOGE4OTI0MWY2OTRhY2U2NjMwYjE0NzhhZDY2Yg"

		dat = requests.get(urls).json()

		for s in dat:
		        if search in s['symbol']:
		                ids = s['id']
		                url = "https://api.coinmarketcal.com/v1/events?access_token=ZmEyMWVmNWM4ZTgzMDAwNjI5NmRkZGYzM2NlMGE5YWI3YzkzOGE4OTI0MWY2OTRhY2U2NjMwYjE0NzhhZDY2Yg&page=1&max=10&coins="+ids+"&sortBy=hot_events"

		                data = requests.get(url).json()
		                name = s['name']
		                symbol = s['symbol']
		                #for i in data:
		                	#title = i["title"]
		                    #	date = i["date_event"] 
		                    #	source = i["source"]
		                    #	dis = i["description"]

		            	return render(request, "dashbord/event.html", {"crypto": crypt , "data": data, "name": name , 'sym': symbol, 'header': event})
						 

	
	return render(request, "dashbord/event.html", {"crypto": crypt, 'header': event })






"""

	sig = Signels.objects.all()
	print sig
	uri = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY="

	api = "a502c1f3-72e0-407a-aa7e-ece644776306"

	url = uri + api

	raw_data = requests.get(url).json()

	data = raw_data['data']

	for i in signel:
		if i.signal_id == 0:
			coin = i.symbol.upper()
			for sym in data:
				if coin in sym['symbol']:
					ids = sym['id']
					i.signal_id = ids
					i.save()
				else: 
					pass
		else:
			pass
				
"""
