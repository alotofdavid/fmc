from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from fmc.models import Scramble
from fmc import views
from django.shortcuts import get_object_or_404
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(
            queryset=Scramble.objects.order_by('-pub_date')[:5],
            context_object_name='latest_scrambles',
            template_name='fmc/index.html'), name='index'),
    url(r'^(?P<scramble_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<scramble_id>\d+)/results/$', views.results, name='results'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<scramble_id>\d+)/submit/$', views.submit, name='submit'),
    url(r'^register/$', 'weekly_fmc.views.register'),
    url(r'^login/$', 'weekly_fmc.views.login'),
    url(r'^auth/$', 'weekly_fmc.views.auth_view'),
    url(r'^logout/$', 'weekly_fmc.views.logout'),
    url(r'^loggedin/$', 'weekly_fmc.views.loggedin'),
    url(r'^invalid/$', 'weekly_fmc.views.invalid'),

)