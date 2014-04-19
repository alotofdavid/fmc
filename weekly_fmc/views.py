from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
import re

USER_REGEX = re.compile("[:alnum:]*")

def login(request):
	context = {}
	populateContext(request,context)
	context.update(csrf(request))
	return render_to_response('login.html', context)

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	if user is not None: 
		auth.login(request, user)
		return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/invalid')

def loggedin(request):
	return render_to_response('loggedin.html', {'full_name': request.user.username})

def invalid(request):
	context = {}
	populateContext(request,context)
	context.update(csrf(request))
	return render_to_response('invalid.html', context)

def logout(request):
	auth.logout(request)
	return render_to_response('logout.html')

def profile(request):
	context = {}
	populateContext(request,context)
	context.update(csrf(request))
	return render_to_response('profile.html', context)

def register(request):
	context = {}
	context.update(csrf(request))
	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		password_confirm = request.POST.get('password_confirm', '')
		if password == '' or username == '' or password_confirm == '':
			context['error_message'] = "Please complete all the fields."
		if User.objects.filter(username=username).count():
			context['error_user'] = "Username is already taken"
		if password != password_confirm:
			context['error_pw'] = "Passwords do not match."
			return render_to_response('register.html',context)
		if not USER_REGEX.match(username):
			context['error_user'] = "Invalid username"
			return render_to_response('register.html',context)

		user = User.objects.create_user(username=username, password=password)
		user.save()
		return HttpResponseRedirect('/register_success/')

	return render_to_response('register.html', context)

def register_success(request):
	return render_to_response('register_success.html')

def populateContext(request, context):
	context['authenticated'] = request.user.is_authenticated()
	if context['authenticated'] == True:
		context['user'] = request.user