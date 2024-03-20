# your_app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(CustomUser, UserAdmin)
from django.contrib import admin
from .models import University, College

admin.site.register(University)
admin.site.register(College)
