import uuid
from django.db import models
from user.models import CustomUser


def generate_unique_group_id():
    return uuid.uuid4().hex[:10]


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    group_id = models.CharField(max_length=10, unique=True, default=generate_unique_group_id)
    description = models.TextField()
    members = models.ManyToManyField(CustomUser, related_name='group_members', blank=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='group_creator')
    tags = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name





from django.db import models
from user.models import CustomUser
from social.models import Group

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group, related_name='group_post', blank=True)  # Fix the related_name
    caption = models.TextField()
    post_type = models.CharField(max_length=20, choices=[('normal', 'Normal Post'), ('event', 'Event')])
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
