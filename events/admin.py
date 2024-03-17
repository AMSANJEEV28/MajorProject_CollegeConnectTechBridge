from django.contrib import admin

# Register your models here.
# events/admin.py
from django.contrib import admin
from .models import CollegeEvent

admin.site.register(CollegeEvent)
