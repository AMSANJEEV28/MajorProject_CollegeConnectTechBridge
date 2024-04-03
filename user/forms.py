# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import get_user_model
# from .models import UserProfile

# CustomUser = get_user_model()

# class SignUpForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'password1', 'password2')

# class SignInForm(forms.Form):
#     username = forms.CharField(label='Username')
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'bio', 'university_name', 'college_name', 'registration_id', 'department', 'course', 'profile_picture']
#         widgets = {
#             'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         placeholders = {
#             'first_name': 'Enter your first name',
#             'last_name': 'Enter your last name',
#             'date_of_birth': 'Select your date of birth',
#             'gender': 'Select your gender',
#             'bio': 'Write a brief bio (max 50 words)',
#             'university_name': 'Enter your university name',
#             'college_name': 'Enter your college name',
#             'registration_id': 'Enter your registration ID',
#             'course': 'Enter your course',
#             'department': 'Enter your department',
#             'profile_picture': 'Upload your profile picture',
#         }

#         for field in self.fields:
#             self.fields[field].widget.attrs['placeholder'] = placeholders[field]

















# user/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import UserProfile

CustomUser = get_user_model()

class SignUpForm(UserCreationForm):
    # email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', label='Email', widget=forms.TextInput(attrs={'id': 'id_email_signup', 'placeholder': 'Email'}))  

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

class SignInForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add additional styles to specific fields
        self.fields['email'].widget.attrs['class'] = 'custom-email-field'
        self.fields['password'].widget.attrs['class'] = 'custom-password-field'

from django import forms
from .models import UserProfile

from django import forms
from .models import UserProfile, University, College

class UserProfileForm(forms.ModelForm):
    university_name = forms.ModelChoiceField(queryset=University.objects.all(), empty_label="Select your university")
    college_name = forms.ModelChoiceField(queryset=College.objects.all(), empty_label="Select your college")

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'bio', 'university_name', 'college_name', 'registration_id', 'department', 'course', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'Enter your first name',
            'last_name': 'Enter your last name',
            'date_of_birth': 'Select your date of birth',
            'gender': 'Select your gender',
            'bio': 'Write a brief bio (max 50 words)',
            'registration_id': 'Enter your registration ID',
            'course': 'Enter your course',
            'department': 'Enter your department',
            'profile_picture': 'Upload your profile picture',
        }

        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = placeholders.get(field, '')

        # Set required attribute for all fields except last_name
        for field_name, field in self.fields.items():
            if field_name != 'last_name':
                field.required = True
