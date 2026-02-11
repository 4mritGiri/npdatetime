"""Example forms using Nepali date picker widget"""
from django import forms
from npdt.forms import NepaliDateField, NepaliDateRangeField
from npdt.widgets import NepaliDatePickerWidget
from .models import Person, Event


class PersonForm(forms.ModelForm):
    """Form for creating/editing Person with custom widget"""
    
    class Meta:
        model = Person
        fields = ['name', 'birth_date_bs']
        widgets = {
            'birth_date_bs': NepaliDatePickerWidget(
                mode='BS',
                language='np',
                theme='auto',
                show_today_button=False,
                max_date='2081-12-30'
            )
        }


class EventForm(forms.ModelForm):
    """Form for creating/editing Events"""
    
    class Meta:
        model = Event
        fields = ['title', 'event_type', 'start_date_bs', 'end_date_bs', 'description']
        widgets = {
            'start_date_bs': NepaliDatePickerWidget(
                mode='BS',
                language='en',
                theme='light'
            ),
            'end_date_bs': NepaliDatePickerWidget(
                mode='BS',
                language='en',
                theme='light'
            ),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date_bs')
        end = cleaned_data.get('end_date_bs')
        
        if start and end and end < start:
            raise forms.ValidationError(
                "End date must be after or equal to start date."
            )
        
        return cleaned_data


class DateRangeSearchForm(forms.Form):
    """Example form with date range picker"""
    
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search...'})
    )
    
    date_range = NepaliDateRangeField(
        mode='BS',
        language='en',
        required=False,
        help_text='Select a date range for filtering'
    )
    
    event_type = forms.ChoiceField(
        choices=[('', 'All')] + Event.EVENT_TYPES,
        required=False
    )
