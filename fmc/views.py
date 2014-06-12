# Create your views here.
from django.template import Context, loader
from django.utils import timezone
from fmc.models import Scramble, Submission
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from rubik import *
from django.contrib import messages
from django.contrib.auth.models import User

import datetime

def index(request):
	context = {}
	context.update(csrf(request))
	populateContext(request,context)
	latest_scrambles = Scramble.objects.all().order_by('-pub_date')[:5]
	context['latest_scrambles'] = latest_scrambles
	return render_to_response('fmc/index.html', context)

def about(request):
	context = {}
	context.update(csrf(request))
	populateContext(request,context)
	return render_to_response('fmc/about.html', context)

def detail(request, scramble_id):
	context = {}
	populateContext(request,context)
	context.update(csrf(request))
	s = get_object_or_404(Scramble, pk=scramble_id)
	if (request.user):
		context['name'] = request.user.username
	context['scramble'] = s
	next_id = int(scramble_id) + 1
	prev_id = int(scramble_id) - 1
	next = None
	prev = None
	try:
		prev = Scramble.objects.get(pk=prev_id)
	except Scramble.DoesNotExist:
		pass
	try:
		next = Scramble.objects.get(pk=next_id)
	except Scramble.DoesNotExist:
		pass
	context['next'] = next
	context['prev'] = prev 
	if s.current():
		return render_to_response('fmc/detail.html', context)
	else:
		submissions = s.submission_set.all().order_by('move_count')
		context['submissions'] = submissions
		return render_to_response('fmc/results.html', context)

def submit(request, scramble_id):
	context = {}
	context.update(csrf(request))
	populateContext(request,context)
	s = get_object_or_404(Scramble, pk=scramble_id)
	sol = request.POST['solution']
	name = request.POST['name']
	comments = request.POST['comments']
	context['scramble'] = s
	context['name'] = name
	context['solution'] = sol
	context['comments'] = comments

	if User.objects.filter(username=name).count():
		if name != request.user.username:
			context['name'] = ""
			context['error_message'] = "That name is registered. Please <a href=\"/login/\">log in</a> or choose a different name!"
			return render_to_response('fmc/detail.html', context, context_instance=RequestContext(request))
		if User.objects.filter(username=name)[0].submission_set.all().filter(pk=scramble_id).count():
			context['error_message'] = "You have already submitted a solution to this scramble. Please wait until Sunday (PST) for the next scramble to be posted."
			return render_to_response('fmc/detail.html', context, context_instance=RequestContext(request))

	if not sol or not name:
		context['error_message'] = "Please complete all the fields."
		return render_to_response('fmc/detail.html', context, context_instance=RequestContext(request))
	else:
		if valid_alg(sol):
			alg = Algorithm(sol)
			scr = Algorithm(s.scramble)
			if (scr.solution(alg)):
				move_count = alg.num_moves()
				sub = Submission(solution=sol, name=name,scramble_id=scramble_id, comments=comments, move_count=move_count)
				sub.save()
				
				if (name == request.user.username):
					sub.user_id = request.user.id
					sub.save()	

				return render_to_response('fmc/submit.html', {
					'sub': sub,
					'scramble': s,
					}, context_instance=RequestContext(request))
			else: 
				context['error_message'] = "{sol} does not solve the scramble!".format(sol=sol)
				return render_to_response('fmc/detail.html', context, context_instance=RequestContext(request))
		else:
			context['error_message'] = "{sol} is not a valid algorithm.".format(sol=sol)
			return render_to_response('fmc/detail.html', context, context_instance=RequestContext(request))

def results(request, scramble_id):
	context = {}
	populateContext(request, context)
	s = get_object_or_404(Scramble, pk=scramble_id)
	prev = get_object_or_404(Scramble, pk=scramble_id-1)
	next = get_object_or_404(Scramble, pk=scramble_id+1)
	context['next'] = next
	context['prev'] = prev 
	submissions = s.submission_set.all().order_by('move_count')
	context['scramble'] = s
	context['submissions'] = submissions
	print(prev)
	return render_to_response('fmc/results.html', context)

#in the future i'd like to have a nice way to cache a list of the leaders that gets updated once a week when the scramble is closed. 
def leaders(request):
	context = {}
	populateContext(request, context)
	average_map = {}
	score_map = {}
	users = User.objects.all()
	for u in users:
		submissions = u.submission_set.all()
		completed_subs = [s for s in submissions if not s.scramble.current()]
		if (len(completed_subs) >= 3):
			score = reduce(lambda x,y: x+y, [s.score for s in completed_subs])
			average = reduce(lambda x,y: x+y, [s.move_count for s in completed_subs])/float(len(completed_subs))
			average_map[u] = average
			score_map[u] = score
	context['score_map'] = sorted(score_map.iteritems(), key=lambda (k,v): (v,k), reverse=True)
	context['average_map'] = sorted(average_map.iteritems(), key=lambda (k,v): (v,k))
	return render_to_response('fmc/leaders.html', context)

def populateContext(request, context):
	context['authenticated'] = request.user.is_authenticated()
	if context['authenticated'] == True:
		context['user'] = request.user
