from django.shortcuts import render
from django.shortcuts import redirect 
import requests
# Create your views here.
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from dashboard.models import *
from .models import *
from dashboard.models import *
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



crypt = Dashconf.objects.get()

crypto = {'crypto': crypt}
wname = crypt.site_name


def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None


def register(request):
	
	if request.method == "POST":

		username = request.POST["username"]
		email =  request.POST["email"].lower()
		password = request.POST["password"]
		password2 = request.POST["password2"]
	
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
       	
	return render(request, 'posts/signup.html', {})

def auth_login(request):
	if request.user.is_authenticated():
		return redirect(post)
	else:	
		if request.method == "POST":
			email = request.POST["email"]
			password = request.POST["pass"]
			username = get_user(email)
			

			user = authenticate(username=username , password=password)
			
			if user is not None:			
				if user.profile.email_confirmed:	
					login(request, user)

					return redirect(post)
				else:
					messages.info(request, "email is not confirmed.")	
			else:
				messages.error(request, "password yesn't match")

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


@login_required(login_url= "/login/")
def post(request):
	crypt = Dashconf.objects.get()
	signel = Signels.objects.all()

	dash = "Posts"

	for i in signel:
		if i.signal_id == 0:
			coin = i.symbol.upper()
			coincap(request, coin , i)
		else:
			pass

	return render(request, 'posts/all.html', {"crypto": crypt , "signels" : reversed(signel), "header": dash } ) 



def profile(request, username):
	crypt = Dashconf.objects.get()
	user = User.objects.get(username=username)
	signel = Signels.objects.filter(author=user)
	dash = "Profile"


	return render(request, 'posts/profile.html', {"user": user, "crypto": crypt , "signels" : reversed(signel), "header": dash })





def editProfile(request):
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



def logout(request):
	try:
		for i in request.session.keys():
			del request.session[i]
			return redirect(auth_login)
   	except:
   		pass
	
   	

class PostCreate(LoginRequiredMixin, CreateView):
	model = Signels
	success_url = '/posts'
	fields = ['coin_name', 'symbol', 'title', 'buy', 'sell', 'stop_loss' , 'trade_time' , 'Exchange']
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(PostCreate, self).form_valid(form)


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