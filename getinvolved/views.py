from django.shortcuts import render
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings


def alumni_network_view(request):
    # Your view logic here
    return render(request, 'alumni_network.html')