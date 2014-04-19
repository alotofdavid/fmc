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

import datetime

def index(request):
	context = {}
	context.update(csrf(request))
	populateContext(request,context)
	latest_scrambles = Scramble.objects.all().order_by('-pub_date')[:5]
	context['latest_scrambles'] = latest_scrambles
	return render_to_response('fmc/index.html', context)

def detail(request, scramble_id):
	context = {}
	populateContext(request,context)
	context.update(csrf(request))
	s = get_object_or_404(Scramble, pk=scramble_id)
	context['scramble'] = s
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
				latest_scrambles = Scramble.objects.all().order_by('-pub_date')[:5]
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
	submissions = s.submission_set.all().order_by('move_count')
	context['scramble'] = s
	context['submissions'] = submissions
	return render_to_response('fmc/results.html', context)

def populateContext(request, context):
	context['authenticated'] = request.user.is_authenticated()
	if context['authenticated'] == True:
		context['user'] = request.user
