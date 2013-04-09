# Create your views here.

from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView
from reviews.forms import BusinessForm

from reviews.models import Business
from reviews.models import Category

from django.utils import timezone
from django.views.generic.base import View

from django.contrib.auth import authenticate, login

def home(request):
    context = {}
    return render(request, 'reviews/index.html', context)

def user(request):
    context = {}
    return render(request, 'reviews/user/view.html', context)

class RegisterUser(View):
    def post(self, request, *args, **kwargs):
        user_form = UserCreateForm(request.POST)
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username,
                                password=password)
            login(request, user)
            return redirect("somewhere")
        return render(request,
                      self.template_name,
                      { 'user_form' : user_form })

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

def category(request):
    top_category_list = Category.objects.order_by('name')[:10]
    context = {'top_category_list': top_category_list}
    return render(request, 'reviews/templates/reviews/index.html', context)

class BusinessCreate(CreateView):
    form_class = BusinessForm
    model = Business

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BusinessCreate, self).form_valid(form)

class BusinessUpdate(UpdateView):
    form_class = BusinessForm
    model = Business

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BusinessUpdate, self).form_valid(form)

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
