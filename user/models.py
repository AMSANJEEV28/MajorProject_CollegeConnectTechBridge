# user/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add custom fields if needed
    pass

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    bio = models.TextField(max_length=50, blank=True, null=True)
    university_name = models.CharField(max_length=100)
    college_name = models.CharField(max_length=100)
    registration_id = models.CharField(max_length=20)
    course = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default_profile_picture.jpg', blank=True, null=True)

    def __str__(self):
        return self.user.username
