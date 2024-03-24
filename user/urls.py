# user/urls.py
from django.urls import path
from .views import signup, signin, signout, create_profile, profile, edit_profile
from django.urls import path
from . import views 
from .views import linkedin_signup
from django.urls import path
from .views import linkedin_signup, CustomOAuth2LoginView

from django.urls import path
from user.views import CustomOAuth2LoginView




app_name = 'user'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('create-profile/', create_profile, name='create_profile'),
    path('profile/', profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'), 

    path('linkedin/signup/', linkedin_signup, name='linkedin_signup'),
    path('linkedin/login/', CustomOAuth2LoginView.as_view(), name='oauth2_login'),

]


