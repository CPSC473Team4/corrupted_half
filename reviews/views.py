# Create your views here.

from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from reviews.models import Business

from django.utils import timezone
# from django.views.generic.base import View

from django.contrib.auth import authenticate, login

def home(request):
    context = {}
    return render(request, 'reviews/index.html', context)

def user(request):
    context = {}
    return render(request, 'reviews/user/view.html', context)

class BusinessListView(ListView):
	model = Business

	def get_context_data(self, **kwargs):
		business_list = Business.objects.all()
		paginator = Paginator(business_list, 25)

		page = self.request.GET.get('page')
		try:
			businesses = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			businesses = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			businesses = paginator.page(paginator.num_pages)

		context = super(BusinessListView, self).get_context_data(**kwargs)

		context['businesses'] = businesses
		return context

def auth(request, action):
	if request.method == 'POST':
		if action == 'login':
			username = request.POST['username']
			password = request.POST['password']

			user = authenticate(username=username, password=password)

			if user is not None:
				print(user.first_name)

				if user.is_active:
					login(request, user)
					return redirect('/')
				else:
					# Disabled account
					pass
			else:
				# Return an invalid login error message
				pass
	else:
		if action == 'login':
			return render(request, 'reviews/auth/login.html', {})
		else:
			return render(request, 'reviews/auth/logout.html', {})
