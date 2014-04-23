from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
import re

USER_REGEX = re.compile("^[a-zA-z0-9]+$")

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
		return HttpResponseRedirect(reverse('index'))
	else:
		return HttpResponseRedirect(reverse('invalid'))

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

def profile(request, user_id):
	context = {}
	populateContext(request, context)
	if not User.objects.filter(id=user_id).count():
		return render_to_response('profile_404.html', context)
	profile_user = User.objects.filter(id=user_id)[0]
	context['profile_user'] = profile_user
	submissions = profile_user.submission_set.all().order_by('move_count')
	completed_subs = [s for s in submissions if not s.scramble.current()]
	context['submissions'] = completed_subs
	return render_to_response('profile.html', context)

def profile_edit(request):
	context = {}
	populateContext(request, context)
	context.update(csrf(request))
	if request.method == 'POST':
		username = request.user
		password = request.POST['current_pass']
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			new_pass = request.POST['new_pass']
			new_pass2 = request.POST['new_pass2']
			if new_pass != new_pass2:
				context['error_message'] = "Passwords do not match!"
				return render_to_response('profile_edit.html', context)		
			user.set_password(new_pass)
			user.save()
			return HttpResponseRedirect(reverse('profile_pass'))
		context['error_message'] = "Password is incorrect"
		return render_to_response('profile_edit.html',context)

	return render_to_response('profile_edit.html', context)

	context = {}
	populateContext(request, context)

def profile_pass(request):
	context = {}
	populateContext(request, context)
	return render_to_response('profile_pass.html', context)

def register(request):
	context = {}
	context.update(csrf(request))

	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		password_confirm = request.POST.get('password_confirm', '')
		if password == '' or username == '' or password_confirm == '':
			context['error_message'] = "Please complete all the fields."
			return render_to_response('register.html',context)
		if User.objects.filter(username=username).count():
			context['error_user'] = "Username is already taken"
			return render_to_response('register.html',context)
		if password != password_confirm:
			context['error_pw'] = "Passwords do not match."
			return render_to_response('register.html',context)
		if not USER_REGEX.match(username):
			context['error_user'] = "Invalid username"
			return render_to_response('register.html',context)

		user = User.objects.create_user(username=username, password=password)
		user.save()
		return HttpResponseRedirect(reverse('register_success'))

	return render_to_response('register.html', context)

def register_success(request):
	return render_to_response('register_success.html')

def populateContext(request, context):
	context['authenticated'] = request.user.is_authenticated()
	if context['authenticated'] == True:
		context['user'] = request.user