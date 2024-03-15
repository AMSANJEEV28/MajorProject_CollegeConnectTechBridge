# user/urls.py
from django.urls import path
from .views import signup, signin, signout, create_profile, profile, edit_profile

app_name = 'user'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('create-profile/', create_profile, name='create_profile'),
    path('profile/', profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'), 
    # Add other URLs as needed
]
