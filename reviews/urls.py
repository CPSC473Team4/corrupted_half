from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^starter/', 'reviews.views.starter'),
	url(r'^marketing/', 'reviews.views.marketing'),
)