from django.shortcuts import render

# def contactinfo_view(request):
#     # Your view logic here
#     return render(request, 'contactinfo.html')

from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

def contactinfo_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send email
        subject = 'New Enquiry from Contact Us Page'
        body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        sender_email = settings.EMAIL_HOST_USER
        recipient_email = ['206320028@gkv.ac.in']  # Your email address to receive enquiries
        send_mail(subject, body, sender_email, recipient_email)

        # Send confirmation email to user
        confirmation_subject = 'Thank You for Contacting Us'
        confirmation_body = 'Thank you for contacting us. We have received your enquiry and will get back to you soon.'
        send_mail(confirmation_subject, confirmation_body, sender_email, [email])

        # Optionally, we can add a confirmation message or redirect to a thank you page
        # For example:
        # return render(request, 'thank_you.html')
        # or
        # return redirect('thank_you_page')


    return render(request, 'contactinfo.html')


def faq_view(request):
    # Your view logic here
    return render(request, 'faq.html')

def support_view(request):
    # Your view logic here
    return render(request, 'support.html')