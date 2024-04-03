# user/urls.py
from django.urls import path
from .views import signup, signin, signout, create_profile, profile, edit_profile, verify_otp
from django.urls import path
from . import views 



app_name = 'user'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('create-profile/', create_profile, name='create_profile'),
    path('accounts/profile/', views.profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'), 
    path('verify_otp/', verify_otp, name='verify_otp'),


]


