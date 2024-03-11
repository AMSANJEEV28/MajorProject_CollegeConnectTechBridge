# home/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

