"""Custom form fields for Nepali dates"""

import re

from django import forms
from django.core.exceptions import ValidationError

try:
    from npdatetime import NepaliDate

    NPDATETIME_AVAILABLE = True
except ImportError:
    NPDATETIME_AVAILABLE = False

from .widgets import NepaliDatePickerWidget, NepaliDateRangeWidget


class NepaliDateField(forms.CharField):
    """A form field for Nepali (Bikram Sambat) dates.

    Supports all dynamic widget options. Pass them via ``widget_kwargs``
    or directly as keyword arguments.

    Args:
        mode (str): 'BS' or 'AD'. Default: 'BS'
        language (str): 'en' or 'np'. Default: 'en'
        widget_kwargs (dict): Extra keyword arguments forwarded to
            NepaliDatePickerWidget. Supports disabled_dates,
            disable_past_dates, disable_holidays, holiday_provider,
            disable_weekends, admin_theme, etc.

    Example::

        class LeaveForm(forms.Form):
            start_date = NepaliDateField(
                widget_kwargs={
                    'disable_past_dates': True,
                    'disable_holidays': True,
                    'disable_weekends': True,
                }
            )
    """

    def __init__(self, *args, mode="BS", language="en", widget_kwargs=None, **kwargs):
        self.mode = mode
        self.language = language

        # Build widget kwargs
        wkw = {"mode": mode, "language": language}
        if widget_kwargs:
            wkw.update(widget_kwargs)

        if "widget" not in kwargs:
            kwargs["widget"] = NepaliDatePickerWidget(**wkw)

        kwargs.setdefault("max_length", 10)

        super().__init__(*args, **kwargs)

    def clean(self, value):
        """Validate and clean the date value."""
        value = super().clean(value)

        if not value:
            return value

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
            raise ValidationError(
                "Enter a valid date in YYYY-MM-DD format.", code="invalid_format"
            )

        if NPDATETIME_AVAILABLE:
            try:
                year, month, day = map(int, value.split("-"))
                if self.mode == "BS":
                    NepaliDate(year, month, day)
                else:
                    NepaliDate.from_gregorian(year, month, day)
            except Exception as e:
                raise ValidationError(
                    f"Invalid {self.mode} date: {e}", code="invalid_date"
                )

        return value

    def to_nepali_date(self, value):
        """Convert the cleaned value to a NepaliDate instance."""
        if not value or not NPDATETIME_AVAILABLE:
            return None

        year, month, day = map(int, value.split("-"))
        if self.mode == "BS":
            return NepaliDate(year, month, day)
        else:
            return NepaliDate.from_gregorian(year, month, day)


# Aliases
NpDateField = NepaliDateField
NpDate = NepaliDateField


class NepaliDateTimeField(forms.CharField):
    """A form field for Nepali dates with time.

    Args:
        mode (str): 'BS' or 'AD'. Default: 'BS'
        language (str): 'en' or 'np'. Default: 'en'
        widget_kwargs (dict): Extra keyword arguments forwarded to widget.
    """

    def __init__(self, *args, mode="BS", language="en", widget_kwargs=None, **kwargs):
        self.mode = mode
        self.language = language

        wkw = {"mode": mode, "language": language, "include_time": True}
        if widget_kwargs:
            wkw.update(widget_kwargs)

        if "widget" not in kwargs:
            kwargs["widget"] = NepaliDatePickerWidget(**wkw)

        kwargs.setdefault("max_length", 19)

        super().__init__(*args, **kwargs)

    def clean(self, value):
        """Validate and clean the datetime value."""
        value = super().clean(value)

        if not value:
            return value

        if not re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}(:\d{2})?$", value):
            raise ValidationError(
                "Enter a valid datetime in YYYY-MM-DD HH:MM:SS format.",
                code="invalid_format",
            )

        if value.count(":") == 1:
            value += ":00"

        if NPDATETIME_AVAILABLE:
            try:
                date_part = value.split(" ")[0]
                year, month, day = map(int, date_part.split("-"))
                if self.mode == "BS":
                    NepaliDate(year, month, day)
                else:
                    NepaliDate.from_gregorian(year, month, day)

                time_part = value.split(" ")[1]
                hour, minute, second = map(int, time_part.split(":"))
                if not (0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60):
                    raise ValueError("Invalid time values")

            except Exception as e:
                raise ValidationError(
                    f"Invalid {self.mode} datetime: {e}", code="invalid_datetime"
                )

        return value


# Aliases
NpDateTimeField = NepaliDateTimeField
NpDateTime = NepaliDateTimeField


class NepaliDateRangeField(forms.CharField):
    """A form field for selecting a Nepali date range.

    Args:
        mode (str): 'BS' or 'AD'. Default: 'BS'
        language (str): 'en' or 'np'. Default: 'en'
        widget_kwargs (dict): Extra keyword arguments forwarded to widget.
    """

    def __init__(self, *args, mode="BS", language="en", widget_kwargs=None, **kwargs):
        self.mode = mode
        self.language = language

        wkw = {"mode": mode, "language": language}
        if widget_kwargs:
            wkw.update(widget_kwargs)

        if "widget" not in kwargs:
            kwargs["widget"] = NepaliDateRangeWidget(**wkw)

        super().__init__(*args, **kwargs)

    def clean(self, value):
        """Validate the date range."""
        value = super().clean(value)

        if not value:
            return value

        if " to " not in value:
            raise ValidationError(
                "Enter a valid date range in format: YYYY-MM-DD to YYYY-MM-DD",
                code="invalid_format",
            )

        start_date, end_date = value.split(" to ")

        for date_str in [start_date, end_date]:
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
                raise ValidationError(
                    "Invalid date format in range. Use YYYY-MM-DD.",
                    code="invalid_format",
                )

        if start_date > end_date:
            raise ValidationError(
                "Start date must be before or equal to end date.", code="invalid_range"
            )

        return value

    def get_date_range(self, value):
        """Return tuple of (start_date, end_date) as strings."""
        if not value or " to " not in value:
            return (None, None)

        return tuple(value.split(" to "))
