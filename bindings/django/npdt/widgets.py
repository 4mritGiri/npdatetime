"""Custom widgets for Nepali date picker.

Provides enterprise-grade, fully reusable date picker widgets with
dynamic configuration options for disabling dates, holidays, past
dates, specific weekdays, and custom validation callbacks.
"""

import json

from django import forms
from django.forms.widgets import Input
from django.utils.safestring import mark_safe

from .holidays import HolidayProvider, NepalPublicHolidays


def _normalize_disabled_days(value):
    """Normalize disabled_days to a list of ints.

    Accepts multiple formats:
    - list[int]: [0, 6] -> [0, 6]
    - str comma-separated: "0,6" -> [0, 6]
    - str range: "1-5" -> [1, 2, 3, 4, 5]
    - str mixed: "1-5,0" -> [1, 2, 3, 4, 5, 0]
    - None: -> []

    Weekday convention: 0=Sunday, 1=Monday, ..., 6=Saturday
    """
    if not value:
        return []

    if isinstance(value, (list, tuple)):
        return [int(d) for d in value]

    if isinstance(value, str):
        result = []
        for part in value.split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                try:
                    start, end = part.split("-", 1)
                    start, end = int(start.strip()), int(end.strip())
                    result.extend(range(start, end + 1))
                except (ValueError, TypeError):
                    continue
            else:
                try:
                    result.append(int(part))
                except (ValueError, TypeError):
                    continue
        return result

    return []


class NepaliDatePickerWidget(Input):
    """A widget that renders a Nepali date picker.

    Supports dynamic configuration for enterprise use cases:
    - Disable specific dates (holidays, blackout dates)
    - Disable past dates (future-only selection)
    - Disable specific weekdays (e.g., Saturdays)
    - Custom holiday providers
    - Custom date-disabled callbacks
    - Django admin theme integration

    Args:
        mode (str): 'BS' for Bikram Sambat or 'AD' for Gregorian. Default: 'BS'
        language (str): 'en' for English or 'np' for Nepali. Default: 'en'
        include_time (bool): Whether to include time selection. Default: False
        format (str): Date format string. Default: '%Y-%m-%d'
        theme (str): 'auto', 'light', 'dark', or 'admin'. Default: 'auto'
        show_today_button (bool): Show the "Today" button. Default: True
        show_clear_button (bool): Show the "Clear" button. Default: True
        min_date (str): Minimum selectable date in YYYY-MM-DD format
        max_date (str): Maximum selectable date in YYYY-MM-DD format
        disabled_dates (list[str]): List of date strings to disable (YYYY-MM-DD)
        disabled_days (list[int] | str): Weekday indices to disable.
            Supports: list [0,6], range "1-5" (Mon-Fri), mixed "1-5,0".
            0=Sunday, 1=Monday, ..., 6=Saturday
        disable_past_dates (bool): Disable all dates before today. Default: False
        disable_holidays (bool): Disable holidays from holiday_provider. Default: False
        holiday_provider (HolidayProvider): Provider for holiday data.
            Default: NepalPublicHolidays when disable_holidays=True
        show_holidays (bool): Highlight holidays visually (without disabling). Default: True
        disable_weekends (bool): Disable weekends (Sat in BS, Sun in AD). Default: False
        on_date_disabled (str): Behavior when a disabled date is selected:
            'prevent' - prevent selection entirely (default)
            'warn' - allow selection with a warning
        admin_theme (bool): Alias for theme='admin'. Default: False

    Example::

        # Future dates only, no weekends
        widget = NepaliDatePickerWidget(
            disable_past_dates=True,
            disable_weekends=True,
        )

        # Custom holidays + disabled dates
        widget = NepaliDatePickerWidget(
            disabled_dates=['2082-01-15', '2082-06-20'],
            holiday_provider=MyCompanyHolidays(),
            disable_holidays=True,
        )

        # Admin theme
        widget = NepaliDatePickerWidget(admin_theme=True)
    """

    input_type = "text"
    template_name = "npdt/widgets/picker.html"

    class Media:
        css = {"all": ("npdt/css/picker.css",)}
        js = ("npdt/js/picker.min.js",)

    def __init__(
        self,
        attrs=None,
        mode="BS",
        language="en",
        include_time=False,
        format="%Y-%m-%d",
        theme="auto",
        show_today_button=True,
        show_clear_button=True,
        min_date=None,
        max_date=None,
        disabled_dates=None,
        disabled_days=None,
        disable_past_dates=False,
        disable_holidays=False,
        holiday_provider=None,
        show_holidays=True,
        disable_weekends=False,
        on_date_disabled="prevent",
        admin_theme=False,
        **kwargs,
    ):
        super().__init__(attrs)

        self.mode = mode
        self.language = language
        self.include_time = include_time
        self.format = format
        self.theme = "admin" if admin_theme else theme
        self.show_today_button = show_today_button
        self.show_clear_button = show_clear_button
        self.min_date = min_date
        self.max_date = max_date
        self.disabled_dates = disabled_dates or []
        self.disabled_days = _normalize_disabled_days(disabled_days)
        self.disable_past_dates = disable_past_dates
        self.disable_holidays = disable_holidays
        self.holiday_provider = holiday_provider
        self.show_holidays = show_holidays
        self.disable_weekends = disable_weekends
        self.on_date_disabled = on_date_disabled
        self.extra_options = kwargs

    def _get_holiday_dates(self):
        """Resolve holiday dates from the provider for the widget options."""
        if not self.holiday_provider and not self.disable_holidays:
            return []

        provider = self.holiday_provider
        if provider is None and self.disable_holidays:
            provider = NepalPublicHolidays()

        if not isinstance(provider, HolidayProvider):
            return []

        try:
            import npdatetime

            today = npdatetime.NepaliDate.today()
            # Get holidays for a range of years around current
            holidays = []
            for year in range(today.year - 1, today.year + 3):
                holidays.extend(provider.get_holidays(year))
            return [h.date for h in holidays]
        except Exception:
            return []

    def _get_holiday_names(self):
        """Resolve holiday names for tooltip display."""
        if (
            not self.holiday_provider
            and not self.disable_holidays
            and not self.show_holidays
        ):
            return {}

        provider = self.holiday_provider
        if provider is None and (self.disable_holidays or self.show_holidays):
            provider = NepalPublicHolidays()

        if not isinstance(provider, HolidayProvider):
            return {}

        try:
            import npdatetime

            today = npdatetime.NepaliDate.today()
            names = {}
            for year in range(today.year - 1, today.year + 3):
                for h in provider.get_holidays(year):
                    label = h.name_np if self.language == "np" and h.name_np else h.name
                    if label:
                        names[h.date] = label
            return names
        except Exception:
            return {}

    def get_context(self, name, value, attrs):
        """Build the context for rendering the widget template."""
        context = super().get_context(name, value, attrs)

        if attrs is None:
            attrs = {}

        widget_attrs = context["widget"]["attrs"]
        widget_attrs["data-mode"] = self.mode
        widget_attrs["data-language"] = self.language
        widget_attrs["data-theme"] = self.theme
        if self.include_time:
            widget_attrs["data-include-time"] = "true"

        if not widget_attrs.get("class"):
            widget_attrs["class"] = "npd-input"
        else:
            if "npd-input" not in widget_attrs["class"]:
                widget_attrs["class"] += " npd-input"

        # Build picker options
        picker_options = {
            "mode": self.mode,
            "language": self.language,
            "format": self.format,
            "theme": self.theme,
            "showTodayButton": self.show_today_button,
            "showClearButton": self.show_clear_button,
            "includeTime": self.include_time,
        }

        if self.min_date:
            picker_options["minDate"] = self.min_date

        if self.max_date:
            picker_options["maxDate"] = self.max_date

        # Dynamic disabling options
        if self.disabled_dates:
            picker_options["disabledDates"] = self.disabled_dates

        if self.disabled_days:
            picker_options["disabledDays"] = self.disabled_days

        if self.disable_past_dates:
            picker_options["disablePastDates"] = True

        if self.disable_weekends:
            picker_options["disableWeekends"] = True

        if self.disable_holidays:
            holiday_dates = self._get_holiday_dates()
            if holiday_dates:
                # Merge with any existing disabledDates
                existing = picker_options.get("disabledDates", [])
                merged = list(set(existing + holiday_dates))
                picker_options["disabledDates"] = sorted(merged)

        if self.show_holidays:
            holiday_names = self._get_holiday_names()
            if holiday_names:
                picker_options["holidayNames"] = holiday_names

        if self.on_date_disabled != "prevent":
            picker_options["onDateDisabled"] = self.on_date_disabled

        # Add any extra options
        picker_options.update(self.extra_options)

        context["widget"]["picker_options"] = mark_safe(json.dumps(picker_options))
        context["widget"]["include_time"] = self.include_time

        return context

    def build_attrs(self, base_attrs, extra_attrs=None):
        """Build HTML attributes for the widget."""
        attrs = super().build_attrs(base_attrs, extra_attrs)

        attrs["data-mode"] = self.mode
        attrs["data-language"] = self.language
        attrs["data-theme"] = self.theme
        if self.include_time:
            attrs["data-include-time"] = "true"

        attrs["autocomplete"] = "off"

        if "placeholder" not in attrs:
            if self.mode == "BS":
                attrs["placeholder"] = (
                    "मिति (YYYY-MM-DD)" if self.language == "np" else "YYYY-MM-DD"
                )
            else:
                attrs["placeholder"] = "YYYY-MM-DD"

        return attrs


class NepaliDateRangeWidget(forms.MultiWidget):
    """A widget for selecting a date range with two Nepali date pickers.

    Supports all the same dynamic options as NepaliDatePickerWidget.

    Example::

        widget = NepaliDateRangeWidget(
            mode='BS',
            disable_past_dates=True,
            disable_weekends=True,
        )
    """

    template_name = "npdt/widgets/date_range.html"

    def __init__(
        self,
        attrs=None,
        mode="BS",
        language="en",
        disabled_dates=None,
        disabled_days=None,
        disable_past_dates=False,
        disable_holidays=False,
        holiday_provider=None,
        show_holidays=True,
        disable_weekends=False,
        on_date_disabled="prevent",
        admin_theme=False,
        **kwargs,
    ):
        widget_kwargs = {
            "mode": mode,
            "language": language,
            "disabled_dates": disabled_dates,
            "disabled_days": disabled_days,
            "disable_past_dates": disable_past_dates,
            "disable_holidays": disable_holidays,
            "holiday_provider": holiday_provider,
            "show_holidays": show_holidays,
            "disable_weekends": disable_weekends,
            "on_date_disabled": on_date_disabled,
            "admin_theme": admin_theme,
        }
        widget_kwargs.update(kwargs)

        widgets = [
            NepaliDatePickerWidget(attrs=attrs, **widget_kwargs),
            NepaliDatePickerWidget(attrs=attrs, **widget_kwargs),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        """Split the value into start and end dates."""
        if value:
            if " to " in value:
                return value.split(" to ")
            return [value, ""]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        """Combine the two date values into a single range string."""
        values = super().value_from_datadict(data, files, name)
        if values and len(values) == 2 and values[0] and values[1]:
            return f"{values[0]} to {values[1]}"
        return ""
