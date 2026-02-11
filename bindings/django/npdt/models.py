"""Custom model fields for Nepali dates"""
from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
import re

try:
    from npdatetime import NepaliDate
    NPDATETIME_AVAILABLE = True
except ImportError:
    NPDATETIME_AVAILABLE = False


class NepaliDateWrapper(str):
    """
    A string wrapper that provides easy access to Nepali date properties.
    """
    def __new__(cls, value):
        if value is None:
            return None
        return super().__new__(cls, value)

    def __init__(self, value):
        self._date_obj = None
        if not NPDATETIME_AVAILABLE or not value:
            return

        try:
            # Handle YYYY-MM-DD and YYYY-MM-DD HH:MM:SS
            date_part = str(value).split(' ')[0]
            year, month, day = map(int, date_part.split('-'))
            self._date_obj = NepaliDate(year, month, day)
        except Exception:
            pass

    @property
    def fiscal_year(self):
        return self._date_obj.fiscal_year if self._date_obj else None

    @property
    def fiscal_quarter(self):
        return self._date_obj.fiscal_quarter if self._date_obj else None

    @property
    def year(self):
        return self._date_obj.year if self._date_obj else None

    @property
    def month(self):
        return self._date_obj.month if self._date_obj else None

    @property
    def day(self):
        return self._date_obj.day if self._date_obj else None

    @property
    def date_obj(self):
        return self._date_obj


class NepaliDateField(models.CharField):
    """
    A model field for storing Nepali (Bikram Sambat) dates.
    
    Stores dates in YYYY-MM-DD format internally.
    Can be used to create, validate, and convert Nepali dates.
    """
    
    description = "Nepali Date (Bikram Sambat) field"
    
    def __init__(self, *args, mode='BS', language='en', **kwargs):
        self.mode = mode
        self.language = language
        # Force max_length to 10 for YYYY-MM-DD format
        kwargs['max_length'] = 10
        super().__init__(*args, **kwargs)
        
        # Add validator for date format
        self.validators.append(validators.RegexValidator(
            regex=r'^\d{4}-\d{2}-\d{2}$',
            message='Enter a valid Nepali date in YYYY-MM-DD format.',
            code='invalid_nepali_date_format'
        ))
    
    def deconstruct(self):
        """
        Return enough information to recreate the field as a 4-tuple.
        """
        name, path, args, kwargs = super().deconstruct()
        # Remove max_length as we set it automatically
        kwargs.pop('max_length', None)
        if self.mode != 'BS':
            kwargs['mode'] = self.mode
        if self.language != 'en':
            kwargs['language'] = self.language
        return name, path, args, kwargs
    
    def to_python(self, value):
        """
        Convert the input value to a NepaliDate instance or string.
        """
        if value is None or value == '':
            return None
            
        if isinstance(value, str):
            # Validate format
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', value):
                return value
            
            return NepaliDateWrapper(value)
        
        if NPDATETIME_AVAILABLE and isinstance(value, NepaliDate):
            return NepaliDateWrapper(f"{value.year}-{value.month:02d}-{value.day:02d}")
        
        return NepaliDateWrapper(str(value))
    
    def from_db_value(self, value, expression, connection):
        """
        Convert database value to Python value.
        """
        if value is None:
            return value
        return NepaliDateWrapper(value)
    
    def get_prep_value(self, value):
        """
        Convert Python value to database value.
        """
        if value is None or value == '':
            return None
        return str(value)
    
    def formfield(self, **kwargs):
        """
        Return a form field instance for this model field.
        """
        from .forms import NepaliDateField as NepaliDateFormField
        from .widgets import NepaliDatePickerWidget
        
        # If the widget is being overridden by Django Admin (vTextField), 
        # we want to restore ours.
        if 'widget' in kwargs:
            widget = kwargs['widget']
            # Check if it's the admin's default CharField widget
            if hasattr(widget, '__name__') and widget.__name__ == 'AdminCharFieldWidget':
                kwargs['widget'] = NepaliDatePickerWidget(mode=self.mode, language=self.language)
            elif not isinstance(widget, NepaliDatePickerWidget) and not (isinstance(widget, type) and issubclass(widget, NepaliDatePickerWidget)):
                 # If it's not a NepaliDatePickerWidget, we still want to use ours 
                 # but maybe merge some attrs? For now, just force ours.
                 kwargs['widget'] = NepaliDatePickerWidget(mode=self.mode, language=self.language)
        
        defaults = {
            'form_class': NepaliDateFormField,
            'widget': NepaliDatePickerWidget(mode=self.mode, language=self.language),
            'mode': self.mode,
            'language': self.language,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


# Aliases for shorter usage
NpDateField = NepaliDateField
NpDate = NepaliDateField


class NepaliDateTimeField(models.CharField):
    """
    A model field for storing Nepali dates with time.
    
    Stores datetime in YYYY-MM-DD HH:MM:SS format internally.
    """
    
    description = "Nepali DateTime (Bikram Sambat) field"
    
    def __init__(self, *args, mode='BS', language='en', **kwargs):
        self.mode = mode
        self.language = language
        # Force max_length to 19 for YYYY-MM-DD HH:MM:SS format
        kwargs['max_length'] = 19
        super().__init__(*args, **kwargs)
        
        # Add validator for datetime format
        self.validators.append(validators.RegexValidator(
            regex=r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$',
            message='Enter a valid Nepali datetime in YYYY-MM-DD HH:MM:SS format.',
            code='invalid_nepali_datetime_format'
        ))
    
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop('max_length', None)
        if self.mode != 'BS':
            kwargs['mode'] = self.mode
        if self.language != 'en':
            kwargs['language'] = self.language
        return name, path, args, kwargs
    
    def to_python(self, value):
        """Convert input value to valid Nepali datetime string."""
        if value is None or value == '':
            return None
            
        if isinstance(value, str):
            # Validate format
            if not re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', value):
                return value
            
            return NepaliDateWrapper(value)
        
        return NepaliDateWrapper(str(value))
    
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return NepaliDateWrapper(value)
    
    def get_prep_value(self, value):
        if value is None or value == '':
            return None
        return str(value)
    
    def formfield(self, **kwargs):
        """Return a form field instance for this model field."""
        from .forms import NepaliDateTimeField as NepaliDateTimeFormField
        from .widgets import NepaliDatePickerWidget
        
        if 'widget' in kwargs:
            widget = kwargs['widget']
            if hasattr(widget, '__name__') and widget.__name__ == 'AdminCharFieldWidget':
                kwargs['widget'] = NepaliDatePickerWidget(mode=self.mode, language=self.language, include_time=True)
        
        defaults = {
            'form_class': NepaliDateTimeFormField,
            'widget': NepaliDatePickerWidget(mode=self.mode, language=self.language, include_time=True),
            'mode': self.mode,
            'language': self.language,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


# Aliases for shorter usage
NpDateTimeField = NepaliDateTimeField
NpDateTime = NepaliDateTimeField
