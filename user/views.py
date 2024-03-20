from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm, UserProfileForm
from django.contrib.auth import login, logout, authenticate

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


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import SignUpForm
from .models import CustomUser

def signup(request):
    if request.user.is_authenticated:
        # If the user is already authenticated, redirect to the profile page
        return redirect('user:create_profile')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # Check if the email already exists
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists.')
                return redirect('user:signup')

            # Create user if email doesn't exist
            user = CustomUser.objects.create_user(email=email, username=email, password=password)
            login(request, user)
            return redirect('user:create_profile')
        else:
            # If form is not valid, render the signup template with form and errors
            return render(request, 'signup.html', {'form': form})

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignInForm

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignInForm

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

def create_profile(request):
    print("Inside create_profile view")  # Print statement for debugging
    
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
        # If it's a GET request, initialize an empty form
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
