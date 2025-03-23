from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class ProfileFormEdition(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'location', 'website']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False