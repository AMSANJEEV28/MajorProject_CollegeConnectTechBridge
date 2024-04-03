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

# def signup(request):
#     if request.user.is_authenticated:
#         # If the user is already authenticated, redirect to the profile page
#         return redirect('user:create_profile')

#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password1']

#             # Check if the email already exists
#             if CustomUser.objects.filter(email=email).exists():
#                 messages.error(request, 'An account with this email already exists.')
#                 return redirect('user:signup')

#             # Create user if email doesn't exist
#             user = CustomUser.objects.create_user(email=email, username=email, password=password)
#             login(request, user)
#             return redirect('user:create_profile')
#         else:
#             # If form is not valid, render the signup template with form and errors
#             return render(request, 'signup.html', {'form': form})

#     else:
#         form = SignUpForm()

#     return render(request, 'signup.html', {'form': form})




from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout  # Import logout function


from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout  # Add import statement for logout
from .forms import SignUpForm
from .models import CustomUser

from django.contrib.auth import login, authenticate
from django.conf import settings

def signup(request):
    print("Inside signup view")

    if request.user.is_authenticated:
        print("User is already authenticated, redirecting to create_profile")
        return redirect('user:create_profile')

    if request.method == 'POST':
        print("POST request received")
        form = SignUpForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists.')
                return redirect('user:signup')

            user = CustomUser.objects.create_user(email=email, username=email, password=password)

            # Authenticate the user with the proper backend
            user.backend = settings.AUTHENTICATION_BACKENDS[0]

            login(request, user)
            print("User signed up and logged in successfully")
            return redirect('user:create_profile')
        else:
            print("Form is invalid")
            return render(request, 'signup.html', {'form': form})

    else:
        print("GET request received")
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


# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .forms import UserProfileForm

# def create_profile(request):
#     print("Inside create_profile view")  # Print statement for debugging
    
#     # Check if the profile has already been created for the user
#     if not profile_not_created(request.user):
#         messages.warning(request, 'Profile has already been created.')
#         return redirect('home')

#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.user = request.user
#             profile.save()
#             messages.success(request, 'Profile created successfully.')
#             return redirect('home')  # Redirect to home page upon successful profile creation
#         else:
#             # If form is not valid, display error message
#             messages.error(request, 'There was an error with your profile creation. Please correct the errors below.')
#             print("Form errors:", form.errors)  # Print form errors for debugging
#     else:
#         # If it's a GET request, initialize an empty form
#         form = UserProfileForm()

#     # Render the template with the form
#     return render(request, 'create_profile.html', {'form': form})


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







# from django.dispatch import receiver
# from allauth.socialaccount.signals import social_account_added
# from .models import CustomUser, UserProfile

# @receiver(social_account_added)
# def populate_user_profile(sender, request, sociallogin, **kwargs):
#     if sociallogin.account.provider == 'google':
#         user = sociallogin.user
#         extra_data = sociallogin.account.extra_data
        
#         # Update or create the user's profile
#         profile, created = UserProfile.objects.get_or_create(user=user)
        
#         # Populate profile fields with Google data
#         profile.first_name = extra_data.get('given_name', '')
#         profile.last_name = extra_data.get('family_name', '')
#         profile.profile_picture = extra_data.get('picture', '')
        
#         # Save the profile
#         profile.save()
