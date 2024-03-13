# home/urls.py
from django.urls import path
from .views import home, team_view, about, mission, blog

urlpatterns = [
    path('', home, name='home'),
    path('team/', team_view, name='team'),
    path('about/', about, name='about'),
    path('mission/', mission, name='mission'),
    path('blog/', blog, name='blog'),

    
]
