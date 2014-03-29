# Create your views here.
from django.template import Context, loader
from django.utils import timezone
from fmc.models import Scramble, Submission
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse

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
	if not sol or not name:
		return render_to_response('fmc/detail.html', {
			'scramble': s,
			'error_message': "Please complete all the fields.",
			}, context_instance=RequestContext(request))
	else:
		sub = Submission(solution=sol, name=name,scramble_id=scramble_id)
		sub.save()
		return HttpResponseRedirect(reverse('results', args=(s.id,)))

def results(request, scramble_id):
	s = get_object_or_404(Scramble, pk=scramble_id)
	submissions = s.submission_set.all()
	return render_to_response('fmc/results.html', {'scramble': s, 'submissions': submissions})