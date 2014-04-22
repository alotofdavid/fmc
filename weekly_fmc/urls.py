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
    url(r'^register/$', 'weekly_fmc.views.register', name='register'),
    url(r'^login/$', 'weekly_fmc.views.login', name='login'),
    url(r'^auth/$', 'weekly_fmc.views.auth_view', name='auth_view'),
    url(r'^logout/$', 'weekly_fmc.views.logout', name = 'logout'),
    url(r'^loggedin/$', 'weekly_fmc.views.loggedin', name = 'loggedin'),
    url(r'^invalid/$', 'weekly_fmc.views.invalid', name = 'invalid'),
    url(r'^profile/(?P<user_id>\d+)/$', 'weekly_fmc.views.profile', name='profile'),
    url(r'^profile/edit/$', 'weekly_fmc.views.profile_edit', name='profile_edit'),
    url(r'^register_success/$', 'weekly_fmc.views.register_success', name='register_success'),
    url(r'^profile/pass/$', 'weekly_fmc.views.profile_pass', name='profile_pass'),

)