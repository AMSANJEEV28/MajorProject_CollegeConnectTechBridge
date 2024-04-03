from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm, UserProfileForm
from django.contrib.auth import login, logout, authenticate
from .models import CustomUser
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.shortcuts import HttpResponse

# Function to generate OTP
import random
import string
from datetime import datetime, timedelta


def edit_profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            # Redirect to another page after successful form submission
            return redirect('home')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'create_profile.html', {'form': form})


def profile_not_created(user):
    return not hasattr(user, 'userprofile')


# Define the expiration time for the OTP (in minutes)
OTP_EXPIRATION_MINUTES = 2

def generate_otp(length=4):
    otp = ''.join(random.choices(string.digits, k=length))
    # Get the current time
    now = datetime.now()
    # Calculate the expiration time by adding OTP_EXPIRATION_MINUTES to the current time
    expiration_time = now + timedelta(minutes=OTP_EXPIRATION_MINUTES)
    # Return the OTP and its expiration time as a tuple
    return otp, expiration_time

# Usage example
otp, expiration_time = generate_otp()
print("OTP:", otp)
print("Expiration Time:", expiration_time)

from django.contrib.auth import authenticate, login


from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # Check if a user with the provided email already exists
            existing_user = CustomUser.objects.filter(email=email).first()
            if existing_user:
                # If the user exists, redirect to the sign-in page with a message
                messages.info(request, 'An account with this email already exists. Please sign in.')
                return redirect('user:signin')
            else:
                # If the user doesn't exist, proceed with the sign-up process
                otp, expiration_time = generate_otp()

                # Save the OTP and its expiration time in session for verification
                request.session['otp'] = otp
                request.session['otp_expiration_time'] = expiration_time.strftime("%Y-%m-%d %H:%M:%S")
                request.session['email'] = email

                # Send OTP via email
                subject = 'Your OTP for Account Verification'
                message = f'Your OTP is: {otp}. Please use this OTP to sign up on College Connect website. Note that this OTP is valid for {OTP_EXPIRATION_MINUTES} minutes and will expire at {expiration_time}.'
                sender_email = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail(subject, message, sender_email, recipient_list)

                return redirect('user:verify_otp')
        else:
            messages.error(request, 'Invalid form submission. Please try again.')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def verify_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '')
        otp_saved = request.session.get('otp', '')
        expiration_time_str = request.session.get('otp_expiration_time', '')

        # Check if OTP is expired
        if expiration_time_str:
            expiration_time = datetime.strptime(expiration_time_str, "%Y-%m-%d %H:%M:%S")
            if datetime.now() > expiration_time:
                messages.error(request, 'OTP has expired. Please request a new OTP.')
                return redirect('user:signup')

        if otp_entered == otp_saved:
            # If OTP is correct, redirect to create profile page
            return redirect('create_profile')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return HttpResponse("Invalid request method or no OTP entered.")


def signin(request):
    if request.user.is_authenticated:
        # If the user is already authenticated, redirect to the profile page
        return redirect('user:profile')

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authenticate user using email as the username
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)

                if profile_not_created(user):
                    return redirect('user:create_profile')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
        else:
            messages.error(request, 'There was an error with your signin. Please correct the errors below.')
    else:
        form = SignInForm()

    return render(request, 'signin.html', {'form': form})




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserProfileForm
from allauth.socialaccount.models import SocialAccount

@login_required
def create_profile(request):
    # Check if the profile has already been created for the user
    if not profile_not_created(request.user):
        messages.warning(request, 'Profile has already been created.')
        return redirect('home')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully.')
            return redirect('home')  # Redirect to home page upon successful profile creation
        else:
            # If form is not valid, display error message
            messages.error(request, 'There was an error with your profile creation. Please correct the errors below.')
            print("Form errors:", form.errors)  # Print form errors for debugging
    else:
        # If it's a GET request, initialize form with user's Google account information
        try:
            google_account = SocialAccount.objects.get(provider='google', user=request.user)
            google_email = google_account.extra_data.get('email', '')
            google_name = google_account.extra_data.get('name', '')
            google_picture_url = google_account.extra_data.get('picture', '')
            initial_data = {'first_name': google_name, 'email': google_email}
            form = UserProfileForm(initial=initial_data)
            form.fields['profile_picture'].widget.attrs['value'] = google_picture_url  # Pre-fill profile picture URL
        except SocialAccount.DoesNotExist:
            # Handle case where user did not sign up using Google authentication
            form = UserProfileForm()

    # Render the template with the form
    return render(request, 'create_profile.html', {'form': form})



@login_required
def profile(request):
    user_profile = request.user.userprofile
    user_email = request.user.email  # Accessing the email from CustomUser model
    return render(request, 'profile.html', {'user_profile': user_profile, 'user_email': user_email})


def signout(request):
    logout(request)
    return redirect('home')


