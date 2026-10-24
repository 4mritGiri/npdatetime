"""Custom form fields for Nepali dates"""

import re
from datetime import datetime, timezone as datetime_timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

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

    def __init__(self, *args, mode="AD", language="en", widget_kwargs=None, **kwargs):
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

        # Server-side validation for disabled date constraints
        widget = self.widget
        if hasattr(widget, "validate_date"):
            widget.validate_date(value)

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


class NepaliDateTimeField(forms.Field):
    """Parse an AD or BS wall time and return a UTC-aware ``datetime``.

    The picker always displays a value in ``timezone_name`` (Django's current
    timezone by default).  The value returned from ``clean()`` is an instant
    in UTC, so a Django ``DateTimeField`` stores one canonical value regardless
    of whether the user chose AD or BS in the picker.
    """

    input_formats = ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S")

    def __init__(
        self, *args, mode="BS", language="en", timezone_name=None,
        widget_kwargs=None, **kwargs
    ):
        self.mode = mode.upper()
        if self.mode not in {"AD", "BS"}:
            raise ValueError("mode must be either 'AD' or 'BS'")
        self.language = language
        self.timezone_name = timezone_name or timezone.get_current_timezone_name()
        try:
            self.display_timezone = ZoneInfo(self.timezone_name)
        except ZoneInfoNotFoundError as exc:
            raise ValueError(f"Unknown IANA timezone: {self.timezone_name}") from exc

        wkw = {
            "mode": self.mode,
            "language": language,
            "include_time": True,
            "timezone_name": self.timezone_name,
        }
        if widget_kwargs:
            wkw.update(widget_kwargs)
        kwargs.setdefault("widget", NepaliDatePickerWidget(**wkw))
        super().__init__(*args, **kwargs)

    def _parse_local(self, value):
        if not isinstance(value, str):
            raise ValidationError("Enter a valid date and time.", code="invalid_datetime")
        for input_format in self.input_formats:
            try:
                parsed = datetime.strptime(value, input_format)
                break
            except ValueError:
                parsed = None
        if parsed is None:
            raise ValidationError(
                "Enter a valid datetime in YYYY-MM-DD HH:MM or YYYY-MM-DD HH:MM:SS format.",
                code="invalid_format",
            )

        if self.mode == "BS":
            if not NPDATETIME_AVAILABLE:
                raise ValidationError("npdatetime is required for BS dates.", code="npdatetime_unavailable")
            try:
                nepali_date = NepaliDate(parsed.year, parsed.month, parsed.day)
                year, month, day = nepali_date.to_gregorian()
                parsed = parsed.replace(year=year, month=month, day=day)
            except Exception as exc:
                raise ValidationError(f"Invalid BS datetime: {exc}", code="invalid_datetime") from exc

        # ZoneInfo does not reject daylight-saving gaps or folds itself.  A
        # round-trip check means a bank cannot silently book an ambiguous time.
        candidates = []
        for fold in (0, 1):
            candidate = parsed.replace(tzinfo=self.display_timezone, fold=fold)
            utc_value = candidate.astimezone(datetime_timezone.utc)
            if utc_value.astimezone(self.display_timezone).replace(tzinfo=None) == parsed:
                candidates.append(utc_value)
        candidates = list(dict.fromkeys(candidates))
        if not candidates:
            raise ValidationError("This local time does not exist in the selected timezone.", code="nonexistent_time")
        if len(candidates) > 1:
            raise ValidationError("This local time is ambiguous in the selected timezone.", code="ambiguous_time")
        return candidates[0]

    def clean(self, value):
        value = super().clean(value)
        if value in self.empty_values:
            return None
        if isinstance(value, datetime):
            if timezone.is_naive(value):
                return self._parse_local(value.strftime("%Y-%m-%d %H:%M:%S"))
            return value.astimezone(datetime_timezone.utc)
        return self._parse_local(value)

    def prepare_value(self, value):
        """Render stored UTC values in the configured local timezone and calendar."""
        if not isinstance(value, datetime):
            return value
        if timezone.is_naive(value):
            value = timezone.make_aware(value, datetime_timezone.utc)
        local_value = value.astimezone(self.display_timezone)
        if self.mode == "BS" and NPDATETIME_AVAILABLE:
            nepali_date = NepaliDate.from_gregorian(local_value.year, local_value.month, local_value.day)
            date_value = f"{nepali_date.year:04d}-{nepali_date.month:02d}-{nepali_date.day:02d}"
        else:
            date_value = local_value.strftime("%Y-%m-%d")
        return f"{date_value} {local_value:%H:%M:%S}"


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

    def __init__(self, *args, mode="AD", language="en", widget_kwargs=None, **kwargs):
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
