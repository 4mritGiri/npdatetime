"""Custom widgets for Nepali date picker"""
from django import forms
from django.forms.widgets import Input
from django.utils.safestring import mark_safe
import json


class NepaliDatePickerWidget(Input):
    """
    A widget that renders a Nepali date picker.
    
    This widget uses the JavaScript date picker from npdatetime-rust
    to provide a rich, interactive date selection experience.
    
    Args:
        mode (str): 'BS' for Bikram Sambat or 'AD' for Gregorian. Default: 'BS'
        language (str): 'en' for English or 'np' for Nepali. Default: 'en'
        include_time (bool): Whether to include time selection. Default: False
        format (str): Date format string. Default: '%Y-%m-%d'
        theme (str): 'auto', 'light', or 'dark'. Default: 'auto'
        show_today_button (bool): Show the "Today" button. Default: True
        show_clear_button (bool): Show the "Clear" button. Default: True
        min_date (str): Minimum selectable date in YYYY-MM-DD format
        max_date (str): Maximum selectable date in YYYY-MM-DD format
    
    Example:
        class PersonForm(forms.Form):
            birth_date = forms.CharField(
                widget=NepaliDatePickerWidget(
                    mode='BS',
                    language='np',
                    theme='light'
                )
            )
    """
    
    input_type = 'text'
    template_name = 'npdatetime_django/widgets/date_picker.html'
    
    class Media:
        css = {
            'all': ('npdatetime_django/css/date_picker.css',)
        }
        js = (
            'npdatetime_django/js/date_picker.min.js',
        )
    
    def __init__(self, attrs=None, mode='BS', language='en', include_time=False,
                 format='%Y-%m-%d', theme='auto', show_today_button=True,
                 show_clear_button=True, min_date=None, max_date=None, **kwargs):
        super().__init__(attrs)
        
        self.mode = mode
        self.language = language
        self.include_time = include_time
        self.format = format
        self.theme = theme
        self.show_today_button = show_today_button
        self.show_clear_button = show_clear_button
        self.min_date = min_date
        self.max_date = max_date
        self.extra_options = kwargs
    
    def get_context(self, name, value, attrs):
        """Build the context for rendering the widget template."""
        context = super().get_context(name, value, attrs)
        
        # Ensure attrs is not None
        if attrs is None:
            attrs = {}
        
        # Build data attributes for the date picker
        widget_attrs = context['widget']['attrs']
        widget_attrs['data-mode'] = self.mode
        widget_attrs['data-language'] = self.language
        widget_attrs['data-theme'] = self.theme
        if self.include_time:
            widget_attrs['data-include-time'] = 'true'
        
        if not widget_attrs.get('class'):
            widget_attrs['class'] = 'npd-input'
        else:
            if 'npd-input' not in widget_attrs['class']:
                widget_attrs['class'] += ' npd-input'
        
        # Build picker options as JSON
        picker_options = {
            'mode': self.mode,
            'language': self.language,
            'format': self.format,
            'theme': self.theme,
            'showTodayButton': self.show_today_button,
            'showClearButton': self.show_clear_button,
            'includeTime': self.include_time,
        }
        
        if self.min_date:
            picker_options['minDate'] = self.min_date
        
        if self.max_date:
            picker_options['maxDate'] = self.max_date
        
        # Add any extra options
        picker_options.update(self.extra_options)
        
        context['widget']['picker_options'] = mark_safe(json.dumps(picker_options))
        context['widget']['include_time'] = self.include_time
        
        return context
    
    def build_attrs(self, base_attrs, extra_attrs=None):
        """Build HTML attributes for the widget."""
        attrs = super().build_attrs(base_attrs, extra_attrs)
        
        # Add data attributes
        attrs['data-mode'] = self.mode
        attrs['data-language'] = self.language
        attrs['data-theme'] = self.theme
        if self.include_time:
            attrs['data-include-time'] = 'true'
        
        # Set autocomplete off for date pickers
        attrs['autocomplete'] = 'off'
        
        # Add placeholder if not set
        if 'placeholder' not in attrs:
            if self.mode == 'BS':
                attrs['placeholder'] = 'मिति (YYYY-MM-DD)' if self.language == 'np' else 'YYYY-MM-DD'
            else:
                attrs['placeholder'] = 'YYYY-MM-DD'
        
        return attrs


class NepaliDateRangeWidget(forms.MultiWidget):
    """
    A widget for selecting a date range with two Nepali date pickers.
    
    Example:
        class ReportForm(forms.Form):
            date_range = forms.CharField(
                widget=NepaliDateRangeWidget(mode='BS', language='np')
            )
    """
    
    template_name = 'npdatetime_django/widgets/date_range.html'
    
    def __init__(self, attrs=None, mode='BS', language='en', **kwargs):
        widgets = [
            NepaliDatePickerWidget(attrs=attrs, mode=mode, language=language, **kwargs),
            NepaliDatePickerWidget(attrs=attrs, mode=mode, language=language, **kwargs),
        ]
        super().__init__(widgets, attrs)
    
    def decompress(self, value):
        """
        Split the value into start and end dates.
        Expects value in format: "YYYY-MM-DD to YYYY-MM-DD"
        """
        if value:
            if ' to ' in value:
                return value.split(' to ')
            return [value, '']
        return [None, None]
    
    def value_from_datadict(self, data, files, name):
        """Combine the two date values into a single range string."""
        values = super().value_from_datadict(data, files, name)
        if values and len(values) == 2 and values[0] and values[1]:
            return f"{values[0]} to {values[1]}"
        return ''
