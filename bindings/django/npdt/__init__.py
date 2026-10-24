"""
Django NPDateTime - Nepali Date Field and Picker for Django

A Django package that provides Nepali (Bikram Sambat) date field and
a modern, feature-rich date picker widget powered by npdatetime.

Supports dynamic configuration for enterprise use cases:
- Disable specific dates (holidays, blackout dates)
- Disable past dates (future-only selection)
- Disable specific weekdays (e.g., Saturdays)
- Custom holiday providers
- Django admin theme integration
"""

__version__ = "0.2.4"
__author__ = "Amrit Giri"
__email__ = "amritgiri.dev@gmail.com"

default_app_config = "npdt.apps.NpdatetimeDjangoConfig"

from .forms import NepaliDateField as NepaliDateFormField
from .forms import NepaliDateTimeField as NepaliDateTimeFormField
from .holidays import (
    CompositeHolidayProvider,
    HolidayDate,
    HolidayProvider,
    NepalPublicHolidays,
    StaticHolidayProvider,
)
from .models import NepaliDateField, NepaliDateTimeField
from .widgets import NepaliDatePickerWidget

__all__ = [
    "NepaliDateField",
    "NepaliDateTimeField",
    "NepaliDateFormField",
    "NepaliDateTimeFormField",
    "NepaliDatePickerWidget",
    "HolidayProvider",
    "HolidayDate",
    "NepalPublicHolidays",
    "CompositeHolidayProvider",
    "StaticHolidayProvider",
]
