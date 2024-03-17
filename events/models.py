# from django.db import models
# from user.models import CustomUser

# class CollegeEvent(models.Model):
#     CATEGORY_CHOICES = [
#         ('Academic', 'Academic'),
#         ('Art', 'Art'),
#         ('Conference', 'Conference'),
#         ('Cultural', 'Cultural'),
#         ('Music', 'Music'),
#         ('Other', 'Other'),
#         ('Seminar', 'Seminar'),
#         ('Social', 'Social'),
#         ('Sports', 'Sports'),
#         ('Technology', 'Technology'),
#         ('Workshop', 'Workshop'),
#     ]

#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     date_and_time = models.DateTimeField()
#     location = models.CharField(max_length=200)
#     category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
#     organizer = models.CharField(max_length=100)
#     contact_email = models.EmailField()
#     image = models.ImageField(upload_to='event_images/')
#     tags = models.CharField(max_length=100, blank=True)
#     registration_required = models.BooleanField(default=False)
#     registration_deadline = models.DateTimeField(null=True, blank=True)
#     additional_instructions = models.TextField(blank=True)

#     created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


from django.db import models
from user.models import CustomUser

class CollegeEvent(models.Model):
    CATEGORY_CHOICES = [
        ('Academic', 'Academic'),
        ('Art', 'Art'),
        ('Conference', 'Conference'),
        ('Cultural', 'Cultural'),
        ('Music', 'Music'),
        ('Other', 'Other'),
        ('Seminar', 'Seminar'),
        ('Social', 'Social'),
        ('Sports', 'Sports'),
        ('Technology', 'Technology'),
        ('Workshop', 'Workshop'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    date_and_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    organizer = models.CharField(max_length=100)
    contact_email = models.EmailField()
    image = models.ImageField(upload_to='event_images/')
    tags = models.CharField(max_length=100, blank=True)
    registration_required = models.BooleanField(default=False)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    additional_instructions = models.TextField(blank=True)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    participants = models.ManyToManyField(CustomUser, related_name='participated_events', blank=True)
    def __str__(self):
        return self.title
