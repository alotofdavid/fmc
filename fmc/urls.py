from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from fmc.models import Scramble

urlpatterns = patterns('',
    url(r'^/$',
        ListView.as_view(
            queryset=Scramble.objects.order_by('-pub_date')[:5],
            context_object_name='latest_scrambles',
            template_name='fmc/index.html')),
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Scramble,
            template_name='fmc/detail.html')),
)
