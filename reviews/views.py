# Create your views here.

from django.shortcuts import render
from django.conf import settings

def starter(request):
    context = {}
    return render(request, 'reviews/starter.html', context)

def marketing(request):
    context = {}
    return render(request, 'reviews/marketing.html', context)