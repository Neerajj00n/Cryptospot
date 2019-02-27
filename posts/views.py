from django.shortcuts import render
from django.shortcuts import redirect  
import requests
from django.shortcuts import get_list_or_404, get_object_or_404
# Create your views here.
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect , HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from dashboard.models import Dashconfig as Dashconf
from .models import *
from dashboard.models import *
from django.db.models import Count
from django.contrib.sites.shortcuts import get_current_site 
from django.utils.encoding import force_bytes , force_text
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.template.loader import render_to_string
from posts.tokens import account_activation_token
from website.views import coincap
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)



def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None

def register(request):
	crypt = Dashconf.objects.get()
	wname = crypt.site_name

	if request.method == "POST":

		username = request.POST["susername"].lower()
		email =  request.POST["semail"].lower()
		password = request.POST["spassword"]
		password2 = request.POST["spassword2"]
	
 		try:
 			if password2 != password:
				messages.error(request, "password did'nt match")
			elif User.objects.get(email=email):
				messages.error(request, "user with this email already exists")				
		except: 
			if not (User.objects.filter(username=username).exists()): 
				user = User.objects.create_user(username=username, email=email)
				user.set_password(password)
				user.save()
	
				messages.success(request, "user created.")
			else:
				messages.error(request, "Looks like user already exists")


	#			messages.error(request, "Looks like a username with that email or password already exists")
       	
	return HttpResponseRedirect('login')

def auth_login(request):
	if request.user.is_authenticated():
		return redirect(post)
	else:
		crypt = Dashconf.objects.get()	
		if request.method == "POST":
			email = request.POST["username"]
			password = request.POST["password"]
			username = get_user(email)
			

			user = authenticate(username=username , password=password)
			
			if user is not None:			
				login(request, user)

				return HttpResponseRedirect('post')
			else:
				messages.error(request , "password yesn't match")


	return render(request, 'posts/login.html', {"crypto": crypt})

"""
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect(post)
    else:
        return render(request, 'posts/account_activation_invalid.html')
"""


@login_required
def post(request):
	crypt = Dashconf.objects.get()
	dash = "Posts"
	user1 = request.user
	signel = Signels.objects.filter(author__to_user__from_user=request.user)	
	#signel = Signels.objects.filter(author__follow__user=request.user)
	ousers = User.objects.all()
	return render(request, 'posts/all.html', {"ousers":ousers ,"crypto": crypt , "signels" : reversed(signel), "header": dash } ) 
	
	#except:
	#		signel = Signels.objects.all()
	#		return render(request, 'posts/all.html', {"crypto": crypt , "signels" : reversed(signel), "header": dash } )

@login_required
def profile(request, username):
	try:
		crypt = Dashconf.objects.get()
		users = User.objects.get(username=username)
		signel = Signels.objects.filter(author=users) 
		dash = "Profile"
		current_user = request.user
		follower_list = users.profile.get_following(current_user)
		list_count = users.profile.get_following(users)
		followers_count = users.profile.get_followers_count(users)
		
		return render(request, 'posts/profile.html', {'followers_count': followers_count, 'list_count': list_count, 'follower_list': follower_list, "user": users, "crypto": crypt , "signels" : reversed(signel), "header": dash })
	except:
		return HttpResponse("404")

@login_required
def follow(request, pk):
	from_user = request.user
	to_user = User.objects.get(pk=pk)
	followed = Follow(from_user=from_user , to_user=to_user)
	followed.save()

	return HttpResponseRedirect('/{}'.format(to_user.username))

@login_required
def unfollow(request, pk):	
	from_user = request.user
	to_user = User.objects.get(pk=pk)
	followed = Follow.objects.get(from_user=from_user , to_user=to_user)
	followed.delete()

	return HttpResponseRedirect('/{}'.format(to_user.username))	



@login_required
def editProfile(request,username):
	crypt = Dashconf.objects.get()
	ids = request.user.id
	user = User.objects.get(pk=ids)
	if request.method == "POST":	
		
		if "image" in request.FILES:
			image = request.FILES['image'] 	
			user.profile.Propic.save(image.name , image)
			
		else:
			bio = request.POST["bio"]
			first = request.POST["first"]
			last = request.POST["last"]
			Twitter = request.POST["twitter"]
			Telegram = request.POST["telegram"]
		
			user.first_name = first
			user.last_name = last
			user.profile.twitter = Twitter
			user.profile.telegram = Telegram
			user.profile.bio = bio 
			user.profile.save()
			user.save()
 
			
			
	return	render(request, 'posts/edit-profile.html', {"crypto": crypt , 'user' : user})

	
   	

class PostCreate(LoginRequiredMixin, CreateView):
	model = Signels
	extra_context = None
	success_url = '/posts'
	fields = ['coin_name', 'symbol', 'title', 'buy', 'sell', 'stop_loss' , 'trade_time' , 'Exchange', 'values_in']
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(PostCreate, self).form_valid(form)

	def sig(self):
		for i in signel:
			if i.signal_id == 0:
				coin = i.symbol.upper()
				coincap(request, coin , i)
			else:
				pass

	def get_context_data(self, **kwargs):
		kwargs.setdefault('view', self)
		context = super(PostCreate, self).get_context_data(**kwargs)
		context['crypto'] = Dashconf.objects.get()
		context['header'] = 'Create signel'
		return context

class PostEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Signels
	extra_context = None
	success_url = '/posts'
	fields = ['coin_name', 'symbol', 'title', 'buy', 'sell', 'stop_loss' , 'trade_time' , 'Exchange', 'values_in']
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(PostCreate, self).form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

	def get_context_data(self, **kwargs):
		kwargs.setdefault('view', self)
		context = super(PostCreate, self).get_context_data(**kwargs)
		context['crypto'] = Dashconf.objects.get()
		context['header'] = 'Edit signel'
		return context

class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Signels
	extra_context = None
	success_url = '/posts'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

	def get_context_data(self, **kwargs):
		kwargs.setdefault('view', self)
		context = super(PostCreate, self).get_context_data(**kwargs)
		context['crypto'] = Dashconf.objects.get()
		context['header'] = 'Delete signel'
		return context

@login_required
def search(request):
	dash = "search"
	crypt = Dashconf.objects.get()
	if request.method == "POST":
		query = request.POST['search']
		
		
		users = User.objects.filter(username__icontains=query)
		current_user = request.user
		follower_list = current_user.profile.get_following(current_user)
		
		return render(request, 'posts/search.html' ,{ 'follower_list': follower_list, "crypto": crypt, "users": users, 'query': query, "header": dash})
		
		#except:
		#	print 'found nothing'
		#	messages.info(request, "No user found")
		#	return render(request, 'posts/search.html' ,{"crypto": crypt, "header": dash, 'query': query })		



def upvote(request, pk):
	item = Signels.objects.get(pk=pk)
	ids = item.id
	
	if request.user in item.dislike.all():
		item.dislike.remove(request.user)
		item.like.add(request.user)
		item.save()

	elif not request.user in item.like.all():
		item.like.add(request.user)
		item.save()

	else:
		item.like.remove(request.user)
		item.save()
	return redirect(request.META['HTTP_REFERER'])

def downvote(request, pk):
	item = Signels.objects.get(pk=pk)
	ids = item.id
	
	if request.user in item.like.all():
		item.like.remove(request.user)
		item.dislike.add(request.user)
		item.save()

	elif not request.user in item.dislike.all():
		item.dislike.add(request.user)
		item.save()

	else:
		item.dislike.remove(request.user)
		item.save()
	return redirect(request.META['HTTP_REFERER'])



def logout_view(request, username):
	logout(request)
	return redirect(auth_login)	






