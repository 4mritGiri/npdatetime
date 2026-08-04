"""Custom model fields for Nepali dates"""

import re

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models

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
            date_part = str(value).split(" ")[0]
            year, month, day = map(int, date_part.split("-"))
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
    """A model field for storing Nepali (Bikram Sambat) dates.

    Stores dates in YYYY-MM-DD format internally.
    Supports all dynamic widget options passed via ``widget_kwargs``
    on the model field or through ``formfield()``.

    Args:
        mode (str): 'BS' or 'AD'. Default: 'BS'
        language (str): 'en' or 'np'. Default: 'en'
        widget_kwargs (dict): Extra keyword arguments forwarded to
            NepaliDatePickerWidget. Supports disabled_dates,
            disable_past_dates, disable_holidays, holiday_provider,
            disable_weekends, admin_theme, etc.

    Example::

        class LeaveRequest(models.Model):
            # Future dates only, no holidays
            start_date = NepaliDateField(
                widget_kwargs={
                    'disable_past_dates': True,
                    'disable_holidays': True,
                    'disable_weekends': True,
                }
            )

            # Admin-themed with custom disabled dates
            review_date = NepaliDateField(
                widget_kwargs={
                    'admin_theme': True,
                    'disabled_dates': ['2082-01-01', '2082-09-03'],
                }
            )
    """

    description = "Nepali Date (Bikram Sambat) field"

    def __init__(self, *args, mode="BS", language="en", widget_kwargs=None, **kwargs):
        self.mode = mode
        self.language = language
        self.widget_kwargs = widget_kwargs or {}
        kwargs["max_length"] = 10
        super().__init__(*args, **kwargs)

        self.validators.append(
            validators.RegexValidator(
                regex=r"^\d{4}-\d{2}-\d{2}$",
                message="Enter a valid Nepali date in YYYY-MM-DD format.",
                code="invalid_nepali_date_format",
            )
        )

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop("max_length", None)
        if self.mode != "BS":
            kwargs["mode"] = self.mode
        if self.language != "en":
            kwargs["language"] = self.language
        if self.widget_kwargs:
            kwargs["widget_kwargs"] = self.widget_kwargs
        return name, path, args, kwargs

    def to_python(self, value):
        if value is None or value == "":
            return None

        if isinstance(value, str):
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
                return value
            return NepaliDateWrapper(value)

        if NPDATETIME_AVAILABLE and isinstance(value, NepaliDate):
            return NepaliDateWrapper(f"{value.year}-{value.month:02d}-{value.day:02d}")

        return NepaliDateWrapper(str(value))

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return NepaliDateWrapper(value)

    def get_prep_value(self, value):
        if value is None or value == "":
            return None
        return str(value)

    def formfield(self, **kwargs):
        from .forms import NepaliDateField as NepaliDateFormField
        from .widgets import NepaliDatePickerWidget

        # Build widget kwargs from model field config
        widget_kw = {
            "mode": self.mode,
            "language": self.language,
        }
        widget_kw.update(self.widget_kwargs)

        # If a widget was explicitly passed in kwargs, inspect it
        if "widget" in kwargs:
            widget = kwargs["widget"]
            if isinstance(widget, type) and not issubclass(
                widget, NepaliDatePickerWidget
            ):
                kwargs["widget"] = NepaliDatePickerWidget(**widget_kw)
            elif not isinstance(widget, NepaliDatePickerWidget):
                kwargs["widget"] = NepaliDatePickerWidget(**widget_kw)
            # If it's already our widget, let it through

        defaults = {
            "form_class": NepaliDateFormField,
            "widget": NepaliDatePickerWidget(**widget_kw),
            "mode": self.mode,
            "language": self.language,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


# Aliases
NpDateField = NepaliDateField
NpDate = NepaliDateField


class NepaliDateTimeField(models.CharField):
    """A model field for storing Nepali dates with time.

    Stores datetime in YYYY-MM-DD HH:MM:SS format internally.

    Args:
        mode (str): 'BS' or 'AD'. Default: 'BS'
        language (str): 'en' or 'np'. Default: 'en'
        widget_kwargs (dict): Extra keyword arguments forwarded to
            NepaliDatePickerWidget.
    """

    description = "Nepali DateTime (Bikram Sambat) field"

    def __init__(self, *args, mode="BS", language="en", widget_kwargs=None, **kwargs):
        self.mode = mode
        self.language = language
        self.widget_kwargs = widget_kwargs or {}
        kwargs["max_length"] = 19
        super().__init__(*args, **kwargs)

        self.validators.append(
            validators.RegexValidator(
                regex=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",
                message="Enter a valid Nepali datetime in YYYY-MM-DD HH:MM:SS format.",
                code="invalid_nepali_datetime_format",
            )
        )

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop("max_length", None)
        if self.mode != "BS":
            kwargs["mode"] = self.mode
        if self.language != "en":
            kwargs["language"] = self.language
        if self.widget_kwargs:
            kwargs["widget_kwargs"] = self.widget_kwargs
        return name, path, args, kwargs

    def to_python(self, value):
        if value is None or value == "":
            return None

        if isinstance(value, str):
            if not re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", value):
                return value
            return NepaliDateWrapper(value)

        return NepaliDateWrapper(str(value))

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return NepaliDateWrapper(value)

    def get_prep_value(self, value):
        if value is None or value == "":
            return None
        return str(value)

    def formfield(self, **kwargs):
        from .forms import NepaliDateTimeField as NepaliDateTimeFormField
        from .widgets import NepaliDatePickerWidget

        widget_kw = {
            "mode": self.mode,
            "language": self.language,
            "include_time": True,
        }
        widget_kw.update(self.widget_kwargs)

        if "widget" in kwargs:
            widget = kwargs["widget"]
            if isinstance(widget, type) and not issubclass(
                widget, NepaliDatePickerWidget
            ):
                kwargs["widget"] = NepaliDatePickerWidget(**widget_kw)
            elif not isinstance(widget, NepaliDatePickerWidget):
                kwargs["widget"] = NepaliDatePickerWidget(**widget_kw)

        defaults = {
            "form_class": NepaliDateTimeFormField,
            "widget": NepaliDatePickerWidget(**widget_kw),
            "mode": self.mode,
            "language": self.language,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


# Aliases
NpDateTimeField = NepaliDateTimeField
NpDateTime = NepaliDateTimeField
