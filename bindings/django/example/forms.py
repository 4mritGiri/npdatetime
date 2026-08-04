"""Example forms using Nepali date picker widget with dynamic options"""

from django import forms

from npdt.forms import NepaliDateField, NepaliDateRangeField
from npdt.holidays import (
    CompositeHolidayProvider,
    NepalPublicHolidays,
    StaticHolidayProvider,
)
from npdt.widgets import NepaliDatePickerWidget

from .models import BankTransaction, Event, LeaveRequest, Person


class PersonForm(forms.ModelForm):
    """Form for creating/editing Person with custom widget"""

    class Meta:
        model = Person
        fields = ["name", "birth_date_bs"]
        widgets = {
            "birth_date_bs": NepaliDatePickerWidget(
                mode="BS",
                language="np",
                theme="auto",
                show_today_button=False,
                max_date="2081-12-30",
            )
        }


class EventForm(forms.ModelForm):
    """Form for creating/editing Events"""

    class Meta:
        model = Event
        fields = ["title", "event_type", "start_date_bs", "end_date_bs", "description"]
        widgets = {
            "start_date_bs": NepaliDatePickerWidget(
                mode="BS", language="en", theme="light"
            ),
            "end_date_bs": NepaliDatePickerWidget(
                mode="BS", language="en", theme="light"
            ),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date_bs")
        end = cleaned_data.get("end_date_bs")

        if start and end and end < start:
            raise forms.ValidationError(
                "End date must be after or equal to start date."
            )

        return cleaned_data


class LeaveRequestForm(forms.ModelForm):
    """Leave request form — future dates only, no weekends/holidays."""

    class Meta:
        model = LeaveRequest
        fields = ["employee_name", "leave_date", "reason"]
        widgets = {
            "leave_date": NepaliDatePickerWidget(
                disable_past_dates=True,
                disable_weekends=True,
                disable_holidays=True,
                admin_theme=True,
            ),
        }


class BankTransactionForm(forms.ModelForm):
    """Bank transaction form — no holidays, no weekends."""

    class Meta:
        model = BankTransaction
        fields = ["transaction_date", "amount", "description"]
        widgets = {
            "transaction_date": NepaliDatePickerWidget(
                disabled_days=[0, 6],
                disable_holidays=True,
                show_holidays=True,
            ),
        }


class DateRangeSearchForm(forms.Form):
    """Example form with date range picker"""

    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search..."}),
    )

    date_range = NepaliDateRangeField(
        mode="BS",
        language="en",
        required=False,
        help_text="Select a date range for filtering",
        widget_kwargs={
            "disable_past_dates": True,
        },
    )

    event_type = forms.ChoiceField(
        choices=[("", "All")] + Event.EVENT_TYPES, required=False
    )


# --- Standalone form examples (not tied to a model) ---


class FutureDateOnlyForm(forms.Form):
    """Example: Only future dates can be selected."""

    appointment_date = NepaliDateField(
        widget_kwargs={
            "disable_past_dates": True,
            "admin_theme": True,
        }
    )


class NoWeekendsForm(forms.Form):
    """Example: No weekends allowed."""

    working_date = NepaliDateField(
        widget_kwargs={
            "disable_weekends": True,
        }
    )


class CustomDisabledDatesForm(forms.Form):
    """Example: Specific dates disabled (e.g., blackout dates)."""

    booking_date = NepaliDateField(
        widget_kwargs={
            "disabled_dates": ["2082-01-01", "2082-09-03", "2082-10-15"],
            "disable_past_dates": True,
            "admin_theme": True,
        }
    )


class NoHolidaysForm(forms.Form):
    """Example: Nepal public holidays are disabled."""

    submission_date = NepaliDateField(
        widget_kwargs={
            "disable_holidays": True,
            "show_holidays": True,
            "admin_theme": True,
        }
    )


class StrictBusinessDayForm(forms.Form):
    """Example: Only business days (no weekends, no holidays, no past)."""

    report_date = NepaliDateField(
        widget_kwargs={
            "disable_past_dates": True,
            "disable_weekends": True,
            "disable_holidays": True,
            "on_date_disabled": "prevent",
            "admin_theme": True,
        }
    )
