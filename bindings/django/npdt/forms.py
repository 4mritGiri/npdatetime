"""Custom form fields for Nepali dates"""
from django import forms
from django.core.exceptions import ValidationError
import re

try:
    from npdatetime import NepaliDate
    NPDATETIME_AVAILABLE = True
except ImportError:
    NPDATETIME_AVAILABLE = False

from .widgets import NepaliDatePickerWidget, NepaliDateRangeWidget


class NepaliDateField(forms.CharField):
    """
    A form field for Nepali (Bikram Sambat) dates.
    
    Args:
        mode (str): 'BS' or 'AD'. Default: 'BS'
        language (str): 'en' or 'np'. Default: 'en'
        widget: Custom widget. Default: NepaliDatePickerWidget
        **kwargs: Additional arguments passed to CharField
    
    Example:
        class PersonForm(forms.Form):
            birth_date = NepaliDateField(
                mode='BS',
                language='np',
                label='जन्म मिति'
            )
    """
    
    def __init__(self, *args, mode='BS', language='en', **kwargs):
        self.mode = mode
        self.language = language
        
        # Set widget if not provided
        if 'widget' not in kwargs:
            kwargs['widget'] = NepaliDatePickerWidget(
                mode=mode,
                language=language
            )
        
        # Set max length for YYYY-MM-DD format
        kwargs.setdefault('max_length', 10)
        
        super().__init__(*args, **kwargs)
    
    def clean(self, value):
        """Validate and clean the date value."""
        value = super().clean(value)
        
        if not value:
            return value
        
        # Validate format
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', value):
            raise ValidationError(
                'Enter a valid date in YYYY-MM-DD format.',
                code='invalid_format'
            )
        
        # Validate actual date if npdatetime is available
        if NPDATETIME_AVAILABLE:
            try:
                year, month, day = map(int, value.split('-'))
                if self.mode == 'BS':
                    NepaliDate(year, month, day)
                else:
                    # Validate Gregorian date
                    NepaliDate.from_gregorian(year, month, day)
            except Exception as e:
                raise ValidationError(
                    f'Invalid {self.mode} date: {e}',
                    code='invalid_date'
                )
        
        return value
    
    def to_nepali_date(self, value):
        """
        Convert the cleaned value to a NepaliDate instance.
        Returns None if npdatetime is not available or value is empty.
        """
        if not value or not NPDATETIME_AVAILABLE:
            return None
        
        year, month, day = map(int, value.split('-'))
        if self.mode == 'BS':
            return NepaliDate(year, month, day)
        else:
            return NepaliDate.from_gregorian(year, month, day)


# Aliases for shorter usage
NpDateField = NepaliDateField
NpDate = NepaliDateField


class NepaliDateTimeField(forms.CharField):
    """
    A form field for Nepali dates with time.
    
    Args:
        mode (str): 'BS' or 'AD'. Default: 'BS'
        language (str): 'en' or 'np'. Default: 'en'
        **kwargs: Additional arguments passed to CharField
    
    Example:
        class EventForm(forms.Form):
            event_datetime = NepaliDateTimeField(
                mode='BS',
                language='en'
            )
    """
    
    def __init__(self, *args, mode='BS', language='en', **kwargs):
        self.mode = mode
        self.language = language
        
        # Set widget if not provided
        if 'widget' not in kwargs:
            kwargs['widget'] = NepaliDatePickerWidget(
                mode=mode,
                language=language,
                include_time=True
            )
        
        # Set max length for YYYY-MM-DD HH:MM:SS format
        kwargs.setdefault('max_length', 19)
        
        super().__init__(*args, **kwargs)
    
    def clean(self, value):
        """Validate and clean the datetime value."""
        value = super().clean(value)
        
        if not value:
            return value
        
        # Validate format
        if not re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}(:\d{2})?$', value):
            raise ValidationError(
                'Enter a valid datetime in YYYY-MM-DD HH:MM:SS format.',
                code='invalid_format'
            )
        
        # Add seconds if not present
        if value.count(':') == 1:
            value += ':00'
        
        # Validate date part if npdatetime is available
        if NPDATETIME_AVAILABLE:
            try:
                date_part = value.split(' ')[0]
                year, month, day = map(int, date_part.split('-'))
                if self.mode == 'BS':
                    NepaliDate(year, month, day)
                else:
                    NepaliDate.from_gregorian(year, month, day)
                
                # Validate time part
                time_part = value.split(' ')[1]
                hour, minute, second = map(int, time_part.split(':'))
                if not (0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60):
                    raise ValueError("Invalid time values")
                    
            except Exception as e:
                raise ValidationError(
                    f'Invalid {self.mode} datetime: {e}',
                    code='invalid_datetime'
                )
        
        return value


# Aliases for shorter usage
NpDateTimeField = NepaliDateTimeField
NpDateTime = NepaliDateTimeField


class NepaliDateRangeField(forms.CharField):
    """
    A form field for selecting a Nepali date range.
    
    Returns dates in format: "YYYY-MM-DD to YYYY-MM-DD"
    
    Example:
        class ReportForm(forms.Form):
            report_period = NepaliDateRangeField(
                mode='BS',
                language='np'
            )
    """
    
    def __init__(self, *args, mode='BS', language='en', **kwargs):
        self.mode = mode
        self.language = language
        
        if 'widget' not in kwargs:
            kwargs['widget'] = NepaliDateRangeWidget(
                mode=mode,
                language=language
            )
        
        super().__init__(*args, **kwargs)
    
    def clean(self, value):
        """Validate the date range."""
        value = super().clean(value)
        
        if not value:
            return value
        
        if ' to ' not in value:
            raise ValidationError(
                'Enter a valid date range in format: YYYY-MM-DD to YYYY-MM-DD',
                code='invalid_format'
            )
        
        start_date, end_date = value.split(' to ')
        
        # Validate both dates
        for date_str in [start_date, end_date]:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                raise ValidationError(
                    'Invalid date format in range. Use YYYY-MM-DD.',
                    code='invalid_format'
                )
        
        # Validate that start <= end
        if start_date > end_date:
            raise ValidationError(
                'Start date must be before or equal to end date.',
                code='invalid_range'
            )
        
        return value
    
    def get_date_range(self, value):
        """
        Return tuple of (start_date, end_date) as strings.
        Returns (None, None) if value is empty.
        """
        if not value or ' to ' not in value:
            return (None, None)
        
        return tuple(value.split(' to '))
