"""
Django NPDateTime - Nepali Date Field and Picker for Django

A Django package that provides Nepali (Bikram Sambat) date field and 
a modern, feature-rich date picker widget powered by npdatetime-rust.
"""

__version__ = '0.1.0'
__author__ = 'Amrit Giri'
__email__ = 'amritgiri.dev@gmail.com'

default_app_config = 'npdatetime_django.apps.NpdatetimeDjangoConfig'

from .models import NepaliDateField
from .forms import NepaliDateField as NepaliDateFormField
from .widgets import NepaliDatePickerWidget

__all__ = [
    'NepaliDateField',
    'NepaliDateFormField',
    'NepaliDatePickerWidget',
]
