from django.urls import path
from .views import contactinfo_view, faq_view, support_view

app_name="contactus"

urlpatterns = [
    path('contactinfo/', contactinfo_view, name='contactinfo'),
    path('faq/', faq_view, name='faq'),
    path('support/', support_view, name='support'),
    # other paths...
]
