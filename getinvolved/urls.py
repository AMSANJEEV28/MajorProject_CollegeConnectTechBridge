from django.urls import path
from .views import alumni_network_view

app_name="getinvolved"

urlpatterns = [
    path('alumni_network/', alumni_network_view, name='alumni_network'),

]
