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
#from .models import Profile
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from dashboard.models import * 
import requests
from django.core.mail import send_mail, BadHeaderError , EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
import requests
import json
from posts.models import *
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
		
		if firstname == "":
			messages.error(request , "Firstname is empty.")
		
		elif lastname == "":
			messages.error(request , "Lastname is empty.", )		
		elif subject == "":
			messages.error(request , "subject is empty.", )	
		elif messages == "":
			messages.error(request , "message is empty.", )
		
		else:

		 	try:
		 		mail = EmailMessage(subject, msg, email, ['neerajjoon0@gmail.com'], reply_to=[email])
		 		mail.send()
		 	
		 		messages.success(request , "Email sent")
		 		

		 	except BadHeaderError:
		 		messages.error(request , "Email Error.")

	return render(request, 'dashbord/contact.html', {"crypto": crypt , "header": con })



def dashbord(request):
	crypt = get_object_or_404(Dashconf)
	signel = Signels.objects.all()
	listing = Coin_listings.objects.all()
	dash = "Dashboard"

	for i in signel:
		if i.signal_id == 0:
			coin = i.symbol.upper()
			coincap(request, coin , i)
		else:
			pass

	for i in listing:
		if i.coin_id == 0:
			coin = i.cymbol.upper()
			coincap(request, coin , i)
		else:
			pass


	
	return render(request, "dashbord/dashbord.html", {"crypto": crypt , "signels" : reversed(signel), "listing": reversed(listing), "header": dash }) 


def blogs(request):
	crypt = Dashconf.objects.get()
	contact_list = Blog.objects.all()
	pop_list = Blog.objects.all().order_by('-blog_views')
	pop = contact_list[:3]

	paginator = Paginator(contact_list, 4) # Show 25 contacts per page

	page = request.GET.get('page')

	try:
    		blogs = paginator.page(page)
	except PageNotAnInteger:
        	# If page is not an integer, deliver first page.
    		blogs = paginator.page(1)
	except EmptyPage:
        	# If page is out of range (e.g. 9999), deliver last page of results.
    		blogs = paginator.page(paginator.num_pages)

	
	return render(request, "dashbord/blogs.html", {"crypto": crypt, "blog": blogs, 'popular': pop})

def my_blog(request, blog_slug):
	title1=''
	try:
		blog = Blog.objects.get(slug=blog_slug)			
		blog.blog_views = blog.blog_views + 1
		blog.save()
		title1=k.title
	except:
		title1='blog not exist'

	contact_list = Blog.objects.all().order_by('-blog_views')
	pop = contact_list[:3]		


	return render(request, "dashbord/blog_single.html", {'blog': blog, 'popular': pop})


def airdrops(request):
	crypt = Dashconf.objects.get()
	airdrop = Airdrop.objects.all()
	air = "Airdrops"

	return render(request, "dashbord/airdrop.html", {"crypto": crypt , "airdrop": reversed(airdrop), "header": air})


def airdrop_single(request, airdrop_slug):
	crypt = Dashconf.objects.get()
	airdrop = Airdrop.objects.get(slug=airdrop_slug)
	air = "Airdrops"


	return render(request, "dashbord/airdrop-single.html", {"crypto": crypt , "airdrop": airdrop, "header": air})


def shoping(request):
	crypt = Dashconf.objects.get()
	shop  = Shop.objects.all()
	

	sop = "Shop"

	return render(request, "dashbord/shop.html", {"crypto": crypt , "shop": shop , 'header': sop})


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
		
		try: 
			urls = "https://api.coinmarketcal.com/v1/coins?access_token=YTRjNGJiMDQ2MzdkMWI3MzEzYjc5ZDQwYjg1ODIxNmZkMmNkYjlhZmQ3YTU0M2ZkNTBkM2UxMjAxNmViNzBhMg"

			dat = requests.get(urls).json()
			
			for s in dat:
				if search in s['symbol']:
					ids = s['id']
					url = "https://api.coinmarketcal.com/v1/events?access_token=YTRjNGJiMDQ2MzdkMWI3MzEzYjc5ZDQwYjg1ODIxNmZkMmNkYjlhZmQ3YTU0M2ZkNTBkM2UxMjAxNmViNzBhMg&page=1&max=10&coins="+ids+"&sortBy=hot_events"
					data = requests.get(url).json()
					name = s['name']
					symbol = s['symbol']
		                #for i in data:
		                	#title = i["title"]
		                    #	date = i["date_event"] 
		                    #	source = i["source"]
		                    #	dis = i["description"]
					return render(request, "dashbord/event.html", {"srh": search, "crypto": crypt , "data": data, "name": name , 'sym': symbol, 'header': event})
	
		except:
			messages.error(request, '!this service is down, try again later.')
			return render(request, "dashbord/event.html", {"crypto": crypt, 'header': event })
						
	messages.info(request, 'search for crypto events in searchbar.')
	return render(request, "dashbord/event.html", {"crypto": crypt, 'header': event })



def marketcap(request , coin , i):

	uri = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY="

	api = "a502c1f3-72e0-407a-aa7e-ece644776306"

	url = uri + api

	raw_data = requests.get(url).json()

	data = raw_data['data']

	for sym in data:
		if coin in sym['symbol']:
			ids = sym['id']
			i.signal_id = ids
			i.save()
		else: 
			pass

def coincap(request, coin , i):
	try:		
		url = "https://api.coinmarketcap.com/v2/ticker/"

		raw_data = requests.get(url).json()

		data = raw_data['data']

		for s in data:
		     	sym = data[s]['symbol']
		        if coin in sym:
		        	ids = data[s]['id']
		        	
		        	if i.field_exists('coin_id'):
			        		i.coin_id = ids
		        			i.save()
		        	else:
		        		i.signal_id = ids
		        		i.save()
		        
		        else:
		        	pass
	except:
		pass
		
#def posts(request):
#	return render(request , "dashbord/posts.html", {})

"""
def coinevent(request , search):
	crypt = Dashconf.objects.get()
	event = "Coin events"

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
                                    #   date = i["date_event"] 
                                    #   source = i["source"]
                                    #   dis = i["description"]

			return render(request, "dashbord/event.html", {"crypto": crypt , "data": data, "name": name , 'sym': symbol, 'header': event})

"""
