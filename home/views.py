# home/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def team_view(request):
    return render(request, 'team.html')

def about(request):
    return render(request, 'about.html')

def mission(request):
    return render(request, 'mission.html')

def blog(request):
    return render(request, 'blog.html')

