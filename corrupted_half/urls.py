from django.conf.urls import patterns, include, url
from reviews.views import BusinessListView, BusinessCreate, BusinessUpdate
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required

from reviews.models import *
from reviews.forms import BusinessForm, UserCreateForm

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'corrupted_half.views.home', name='home'),
    url(r'^$', 'reviews.views.home'),
	url(r'^home/', 'reviews.views.home'),
	# url(r'^auth/(?P<action>\w+)', 'reviews.views.auth'),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'reviews/auth/login.html'}),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
	url(r'^accounts/user/$', 'reviews.views.user', {}, name='view_user'),
	url(r'^accounts/add/$', CreateView.as_view(model=User, form_class=UserCreateForm), name='user_add'),

	url(r'^businesses/$', BusinessListView.as_view()),
    url(r'^businesses/(?P<pk>\d+)/$', DetailView.as_view(model=Business), name='business_detail'),
    url(r'^businesses/add/$', login_required(CreateView.as_view(model=Business, form_class=BusinessForm)), name='business_add'),
    url(r'^businesses/(?P<pk>\d+)/edit/$', permission_required('business.can_update')(BusinessUpdate.as_view(model=Business, form_class=BusinessForm)), name='business_update'),
    url(r'^businesses/(?P<pk>\d+)/delete/$', permission_required('business.can_delete')(DeleteView.as_view(model=Business)), name='business_delete'),

    url(r'^$', 'reviews.views.category'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
