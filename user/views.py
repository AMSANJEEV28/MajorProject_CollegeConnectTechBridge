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

    return render(request, 'profile.html', {'form': form})


def profile_not_created(user):
    return not hasattr(user, 'userprofile')

def signup(request):
    if request.user.is_authenticated:
        # If the user is already authenticated, redirect to the profile page
        return redirect('user:create_profile')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user:create_profile')
        else:
            messages.error(request, 'There was an error with your signup. Please correct the errors below.')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        # If the user is already authenticated, redirect to the profile page
        return redirect('user:profile')

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                if profile_not_created(user):
                    return redirect('user:create_profile')
                else:
                    return redirect('home')

            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'There was an error with your signin. Please correct the errors below.')
    else:
        form = SignInForm()

    return render(request, 'signin.html', {'form': form})


@login_required
def create_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('home')
        else:
            messages.error(request, 'There was an error with your profile creation. Please correct the errors below.')
    else:
        form = UserProfileForm()

    if not profile_not_created(request.user):
        messages.warning(request, 'Profile has already been created.')
        return redirect('home')

    return render(request, 'create_profile.html', {'form': form})


@login_required
def profile(request):
    user_profile = request.user.userprofile
    return render(request, 'profile.html', {'user_profile': user_profile})


def signout(request):
    logout(request)
    return redirect('home')
