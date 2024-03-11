from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import UserProfile

CustomUser = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')

class SignInForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'bio', 'university_name', 'college_name', 'registration_id', 'department', 'course', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'Enter your first name',
            'last_name': 'Enter your last name',
            'date_of_birth': 'Select your date of birth',
            'gender': 'Select your gender',
            'bio': 'Write a brief bio (max 50 words)',
            'university_name': 'Enter your university name',
            'college_name': 'Enter your college name',
            'registration_id': 'Enter your registration ID',
            'course': 'Enter your course',
            'department': 'Enter your department',
            'profile_picture': 'Upload your profile picture',
        }

        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = placeholders[field]
