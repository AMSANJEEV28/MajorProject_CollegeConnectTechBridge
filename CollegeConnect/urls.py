# CollegeConnect/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views 
from .views import linkedin_signup

from django.urls import path
from .views import linkedin_signup, CustomOAuth2LoginView

from user.views import CustomOAuth2LoginView




urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('social/', include('social.urls')),
    path('career/', include('career.urls')),
    path('blogs/', include('blogs.urls')),
    path('user/', include('user.urls')), 
    path('contactus/', include('contactus.urls')),
    path('getinvolved/', include('getinvolved.urls')),
    path('events/', include('events.urls')),
    
    path('accounts/', include('allauth.urls')),
    path('linkedin/signup/', linkedin_signup, name='linkedin_signup'),
    path('linkedin/login/', CustomOAuth2LoginView.as_view(), name='oauth2_login'),

]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urls.py

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
