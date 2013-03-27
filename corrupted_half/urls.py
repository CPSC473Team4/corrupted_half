from django.conf.urls import patterns, include, url
from reviews.views import AuthLoginView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'corrupted_half.views.home', name='home'),
    url(r'^$', 'reviews.views.home'),
	url(r'^home/', 'reviews.views.home'),
	url(r'^auth/(?P<action>\w+)', 'reviews.views.auth'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
