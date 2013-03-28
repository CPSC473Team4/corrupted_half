# Create your views here.

from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic.base import TemplateView
from django.http import HttpResponse
# from django.views.generic.base import View

from django.contrib.auth import authenticate, login

def home(request):
    context = {}
    return render(request, 'reviews/index.html', context)

def user(request):
    context = {}
    return render(request, 'reviews/user/view.html', context)

class BusinessView(TemplateView):
	template_name = "reviews/business/view.html"

	def get(self, request, *args, **kwargs):
		return HttpResponse('Hello, World!')

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
