from django import forms
from .models import Group, Post


from django import forms
from .models import Group
from taggit.forms import TagField


from django import forms
from .models import Group

class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'tags']



class GroupSearchForm(forms.Form):
    search_query = forms.CharField(label='Search Group')


class GroupJoinForm(forms.Form):
    group_id = forms.CharField(label='Group ID')


# class PostCreationForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['caption', 'post_type', 'image']
        
# social/forms.py

class PostCreationForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.none(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Post
        fields = ['caption', 'post_type', 'image', 'groups']

    def __init__(self, user, *args, **kwargs):
        super(PostCreationForm, self).__init__(*args, **kwargs)
        self.fields['groups'].queryset = user.group_members.all()
