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


class NepaliDateField(models.CharField):
    """
    A model field for storing Nepali (Bikram Sambat) dates.
    
    Stores dates in YYYY-MM-DD format internally.
    Can be used to create, validate, and convert Nepali dates.
    
    Example:
        class Person(models.Model):
            name = models.CharField(max_length=100)
            birth_date_bs = NepaliDateField()
            
        person = Person(name="Ram", birth_date_bs="2081-01-15")
        person.save()
    """
    
    description = "Nepali Date (Bikram Sambat) field"
    
    def __init__(self, *args, **kwargs):
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
                raise ValidationError(
                    '%(value)s is not a valid Nepali date format. Use YYYY-MM-DD.',
                    code='invalid',
                    params={'value': value},
                )
            
            # Validate the actual date if npdatetime is available
            if NPDATETIME_AVAILABLE:
                try:
                    year, month, day = map(int, value.split('-'))
                    NepaliDate(year, month, day)  # Validate
                except Exception as e:
                    raise ValidationError(
                        '%(value)s is not a valid Nepali date: %(error)s',
                        code='invalid',
                        params={'value': value, 'error': str(e)},
                    )
            
            return value
        
        if NPDATETIME_AVAILABLE and isinstance(value, NepaliDate):
            return f"{value.year}-{value.month:02d}-{value.day:02d}"
        
        return str(value)
    
    def from_db_value(self, value, expression, connection):
        """
        Convert database value to Python value.
        """
        return self.to_python(value)
    
    def get_prep_value(self, value):
        """
        Convert Python value to database value.
        """
        value = super().get_prep_value(value)
        return self.to_python(value)
    
    def formfield(self, **kwargs):
        """
        Return a form field instance for this model field.
        """
        from .forms import NepaliDateField as NepaliDateFormField
        from .widgets import NepaliDatePickerWidget
        
        defaults = {
            'form_class': NepaliDateFormField,
            'widget': NepaliDatePickerWidget,
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
    
    Example:
        class Event(models.Model):
            name = models.CharField(max_length=100)
            event_datetime_bs = NepaliDateTimeField()
            
        event = Event(name="Concert", event_datetime_bs="2081-01-15 14:30:00")
        event.save()
    """
    
    description = "Nepali DateTime (Bikram Sambat) field"
    
    def __init__(self, *args, **kwargs):
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
        return name, path, args, kwargs
    
    def to_python(self, value):
        """Convert input value to valid Nepali datetime string."""
        if value is None or value == '':
            return None
            
        if isinstance(value, str):
            # Validate format
            if not re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', value):
                raise ValidationError(
                    '%(value)s is not a valid Nepali datetime format. Use YYYY-MM-DD HH:MM:SS.',
                    code='invalid',
                    params={'value': value},
                )
            
            # Validate the date part if npdatetime is available
            if NPDATETIME_AVAILABLE:
                try:
                    date_part = value.split(' ')[0]
                    year, month, day = map(int, date_part.split('-'))
                    NepaliDate(year, month, day)  # Validate
                except Exception as e:
                    raise ValidationError(
                        '%(value)s contains an invalid Nepali date: %(error)s',
                        code='invalid',
                        params={'value': value, 'error': str(e)},
                    )
            
            return value
        
        return str(value)
    
    def from_db_value(self, value, expression, connection):
        return self.to_python(value)
    
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return self.to_python(value)
    
    def formfield(self, **kwargs):
        """Return a form field instance for this model field."""
        from .forms import NepaliDateTimeField as NepaliDateTimeFormField
        from .widgets import NepaliDatePickerWidget
        
        defaults = {
            'form_class': NepaliDateTimeFormField,
            'widget': NepaliDatePickerWidget(include_time=True),
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


# Aliases for shorter usage
NpDateTimeField = NepaliDateTimeField
NpDateTime = NepaliDateTimeField
