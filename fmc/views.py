# Create your views here.
from django.template import Context, loader
from fmc.models import Scramble
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse

def index(request):
	latest_scrambles = Scramble.objects.all().order_by('-pub_date')[:5]
	return render_to_response('fmc/index.html', { 'latest_scrambles': latest_scrambles })

def root_index(request):
	latest_scrambles = Scramble.objects.all().order_by('-pub_date')[:5]
	return render_to_response('fmc/index.html', { 'latest_scrambles': latest_scrambles })

def detail(request, scramble_id):
    s = get_object_or_404(Scramble, pk=scramble_id)
    return render_to_response('fmc/detail.html', {'scramble': s},context_instance=RequestContext(request))