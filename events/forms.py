from django import forms
from .models import CollegeEvent

class CollegeEventCreationForm(forms.ModelForm):
    class Meta:
        model = CollegeEvent
        fields = ['title', 'description', 'date_and_time', 'location', 'category',
                  'organizer', 'contact_email', 'image', 'tags', 'registration_required',
                  'registration_deadline', 'additional_instructions']
        widgets = {
            'date_and_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set required attribute to True for certain fields
        self.fields['title'].required = True
        self.fields['date_and_time'].required = True
        self.fields['location'].required = True
        self.fields['image'].required = True
