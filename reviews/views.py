# Create your views here.

from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic.base import TemplateView

from django.contrib.auth import authenticate, login

def home(request):
    context = {}
    return render(request, 'reviews/index.html', context)

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


class AuthLoginView(TemplateView):
	template_name = 'reviews/index.html'

	def get(self, request, *args, **kwargs):
		self.render_to_response({})
