from django.conf.urls import patterns, include, url
from reviews.views import BusinessView

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

	url(r'^businesses/', BusinessView.as_view())

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
