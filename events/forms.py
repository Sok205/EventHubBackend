from django import forms
from .models import Event
from datetime import date

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'start_time', 'end_time', 'location', 'max_participants', 'type']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Allows user to select date
        self.fields['date'].widget = forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select a date',
                'min': date.today().isoformat()
            }
        )
        #Allows user to select time
        self.fields['start_time'].widget = forms.TimeInput(
            attrs={
                'type': 'time',
                'class': 'form-control',
                'placeholder': 'Select a time'
            }
        )
        self.fields['end_time'].widget = forms.TimeInput(
            attrs={
                'type': 'time',
                'class': 'form-control',
                'placeholder': 'Select a time'
            }
        )
        for field_name in self.fields:
            if field_name not in ['date', 'start_time']:
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})

