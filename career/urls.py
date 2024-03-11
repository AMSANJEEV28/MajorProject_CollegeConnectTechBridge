from django.urls import path
from .views import academic_view, jobs_view

app_name="career"

urlpatterns = [
    path('academic/', academic_view, name='academic'),
    path('jobs/', jobs_view, name='jobs'),
    # other paths...
]
