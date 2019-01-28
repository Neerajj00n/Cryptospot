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

		username = request.POST["susername"]
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
				current_site = get_current_site(request)
				subject = 'Activate Your {} Account'.format(wname)
				message = render_to_string('account_activation_email.html', {
				'user': user,
                		'domain': current_site.domain,
                		'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                		'token': account_activation_token.make_token(user),
            			})
            			user.email_user(subject, message)
				messages.success(request, "user created. now Activate it from your email")
			else:
				messages.error(request, "Looks like user already exists")


	#			messages.error(request, "Looks like a username with that email or password already exists")
       	
	return HttpResponseRedirect('login')

def auth_login(request):
	if request.user.is_authenticated():
		return redirect(post)
	else:	
		if request.method == "POST":
			email = request.POST["username"]
			password = request.POST["password"]
			username = get_user(email)
			

			user = authenticate(username=username , password=password)
			
			if user is not None:			
				if user.profile.email_confirmed:	
					login(request, user)

					return HttpResponseRedirect('post')
				else:
					messages.info(request , "email is not confirmed.")	
			else:
				messages.error(request , "password yesn't match")

#				messages.error(request, "login fail plz check ur password or email again")


	return render(request, 'posts/login.html', {})


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
		return HttpResponse("hello")

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
		if "bio" in request.POST:

			bio = request.POST["bio"]	
			user.profile.bio = bio 
			user.profile.save()

		elif "image" in request.FILES:
			
			image = request.FILES['image'] 	
			user.profile.Propic.save(image.name , image)

	return	render(request, 'posts/edit-profile.html', {"crypto": crypt , 'user' : user})

	
   	

class PostCreate(LoginRequiredMixin, CreateView):
	model = Signels
	success_url = '/posts'
	fields = ['coin_name', 'symbol', 'title', 'buy', 'sell', 'stop_loss' , 'trade_time' , 'Exchange']
	
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


class PostEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Signels
	success_url = '/posts'
	fields = ['coin_name', 'symbol', 'title', 'buy', 'sell', 'stop_loss' , 'trade_time' , 'Exchange']
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(PostCreate, self).form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Signels
	success_url = '/posts'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

@login_required
def search(request):
	dash = "search"
	crypt = Dashconf.objects.get()
	if request.method == "POST":
		query = request.POST['search']
		
		
		users = User.objects.get(username=query)
		current_user = request.user
		follower_list = users.profile.get_following(current_user)
		return render(request, 'posts/search.html' ,{'follower_list': follower_list, "crypto": crypt, "users": users, 'query': query, "header": dash})
		
		#except:
		#	print 'found nothing'
		#	messages.info(request, "No user found")
		#	return render(request, 'posts/search.html' ,{"crypto": crypt, "header": dash, 'query': query })		


def logout_view(request, username):
	logout(request)
	return redirect(auth_login)	