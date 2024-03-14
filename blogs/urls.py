from django.urls import path
from .views import blog1_view, blog2_view

app_name="blogs"

urlpatterns = [
    path('blog1/', blog1_view, name='blog1'),
    path('blog2/', blog2_view, name='blog2'),
    # other paths...
]
