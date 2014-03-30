# Create your views here.
from django.template import Context, loader
from django.utils import timezone
from fmc.models import Scramble, Submission
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from rubik import *
from django.contrib import messages

import datetime

def index(request):
	latest_scrambles = Scramble.objects.all().order_by('-pub_date')[:5]
	return render_to_response('fmc/index.html', { 'latest_scrambles': latest_scrambles })

def detail(request, scramble_id):
	s = get_object_or_404(Scramble, pk=scramble_id)
	template = loader.get_template('fmc/detail.html')
	context = RequestContext(request, {
		'scramble': s
	})
	return HttpResponse(template.render(context))

def submit(request, scramble_id):
	s = get_object_or_404(Scramble, pk=scramble_id)
	sol = request.POST['solution']
	name = request.POST['name']
	comments = request.POST['comments']
	if not sol or not name:
		return render_to_response('fmc/detail.html', {
			'scramble': s,
			'name': name,
			'solution': sol,
			'comments': comments,
			'error_message': "Please complete all the fields.",
			}, context_instance=RequestContext(request))
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
				return render_to_response('fmc/detail.html', {
					'scramble': s,
					'name': name,
					'solution': sol,
					'comments': comments,
					'error_message': "{sol} does not solve the scramble!".format(sol=sol),
					}, context_instance=RequestContext(request))
		else:
			return render_to_response('fmc/detail.html', {
				'scramble': s,
				'name': name,
				'solution': sol,
				'comments': comments,
				'error_message': "{sol} is not a valid algorithm.".format(sol=sol),
				}, context_instance=RequestContext(request))

def results(request, scramble_id):
	s = get_object_or_404(Scramble, pk=scramble_id)
	submissions = s.submission_set.all()
	return render_to_response('fmc/results.html', {'scramble': s, 'submissions': submissions})

