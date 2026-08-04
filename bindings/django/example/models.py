"""Example models using Nepali date fields with dynamic widget options"""

from django.db import models

from npdt.holidays import HolidayProvider, NepalPublicHolidays
from npdt.models import NepaliDateField, NepaliDateTimeField


class Person(models.Model):
    """Example person model with Nepali date fields"""

    name = models.CharField(max_length=100)
    birth_date_bs = NepaliDateField(help_text="Birth date in Bikram Sambat")
    created_at_bs = NepaliDateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (Born: {self.birth_date_bs})"


class Event(models.Model):
    """Example event model"""

    EVENT_TYPES = [
        ("meeting", "Meeting"),
        ("conference", "Conference"),
        ("workshop", "Workshop"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    start_date_bs = NepaliDateField()
    end_date_bs = NepaliDateField(blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ["-start_date_bs"]

    def __str__(self):
        return f"{self.title} ({self.start_date_bs})"


class LeaveRequest(models.Model):
    """Leave request — future dates only, no weekends/holidays."""

    employee_name = models.CharField(max_length=100)
    leave_date = NepaliDateField(
        widget_kwargs={
            "disable_past_dates": True,
            "disable_weekends": True,
            "disable_holidays": True,
            "admin_theme": True,
        }
    )
    reason = models.TextField(blank=True)

    class Meta:
        verbose_name = "Leave Request"
        verbose_name_plural = "Leave Requests"

    def __str__(self):
        return f"{self.employee_name} - {self.leave_date}"


class BankTransaction(models.Model):
    """Bank transaction — no holidays, no specific weekdays (Sun+Sat off)."""

    transaction_date = NepaliDateField(
        widget_kwargs={
            "disabled_days": [0, 6],  # Disable Sunday and Saturday
            "disable_holidays": True,
            "show_holidays": True,
        }
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Bank Transaction"
        verbose_name_plural = "Bank Transactions"

    def __str__(self):
        return f"{self.transaction_date} - {self.amount}"
