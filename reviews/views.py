# Create your views here.

from django.shortcuts import render
from django.conf import settings

def home(request):
    context = {}
    return render(request, 'reviews/index.html', context)