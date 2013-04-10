# Create your views here.

from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView
from reviews.forms import BusinessForm
from reviews.forms import UserCreateForm

from reviews.models import Business
from reviews.models import Category
from reviews.models import User

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

class SearchView(ListView):
    model = Business
    template_name='reviews/business_list.html'

    def get_context_data(self, **kwargs):

        search = self.request.GET['s'] if 's' in self.request.GET else ''
        category = self.request.GET['category'] if 'category' in self.request.GET else ''

        if category is '':
            business_list = Business.objects.filter(name__icontains=search)
        else:
            business_list = Business.objects.filter(name__icontains=search, category=category)

        paginator = Paginator(business_list, 25)
        categories = Category.objects.all()

        page = self.request.GET.get('page')
        try:
            businesses = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            businesses = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            businesses = paginator.page(paginator.num_pages)

        context = super(SearchView, self).get_context_data(**kwargs)

        context['businesses'] = businesses
        context['categories'] = categories
        context['selected_category'] = category
        return context

class BusinessListView(ListView):
    model = Business

    def get_context_data(self, **kwargs):
        business_list = Business.objects.all()
        paginator = Paginator(business_list, 25)
        categories = Category.objects.all()

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
        context['categories'] = categories
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

##following class is being used to create a the view for creating a new user
##feel free to fix anything I might have done wrong
##took the BusinessCreate class, and followed it as a tempalte for UserCreate
class UserCreate(CreateView):
    form_class = UserCreateForm
    model = User

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UserCreate, self).form_valid(form)



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
