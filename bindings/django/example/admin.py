"""Admin configuration for example models"""

from django.contrib import admin

from .models import BankTransaction, Event, LeaveRequest, Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Admin interface for Person model"""

    list_display = ["name", "birth_date_bs", "created_at_bs"]
    list_filter = ["birth_date_bs"]
    search_fields = ["name"]
    fields = ["name", "birth_date_bs"]

    # The NepaliDatePickerWidget will be automatically used
    # because the model field defines it in formfield()


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for Event model"""

    list_display = ["title", "event_type", "start_date_bs", "end_date_bs"]
    list_filter = ["event_type", "start_date_bs"]
    search_fields = ["title", "description"]

    fieldsets = (
        ("Event Information", {"fields": ("title", "event_type", "description")}),
        (
            "Dates",
            {
                "fields": ("start_date_bs", "end_date_bs"),
                "description": "Enter dates in Bikram Sambat calendar",
            },
        ),
    )


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    """Admin interface for Leave Request — uses admin_theme automatically."""

    list_display = ["employee_name", "leave_date", "reason"]
    list_filter = ["leave_date"]
    search_fields = ["employee_name"]

    # The widget_kwargs on the model field automatically configure:
    # - disable_past_dates=True (can't pick past dates)
    # - disable_weekends=True (can't pick Saturdays)
    # - disable_holidays=True (can't pick Nepal public holidays)
    # - admin_theme=True (matches Django admin design)


@admin.register(BankTransaction)
class BankTransactionAdmin(admin.ModelAdmin):
    """Admin interface for Bank Transaction — no holidays/weekends."""

    list_display = ["transaction_date", "amount", "description"]
    list_filter = ["transaction_date"]
    search_fields = ["description"]

    # The widget_kwargs on the model field automatically configure:
    # - disabled_days=[0, 6] (no Sunday/Saturday)
    # - disable_holidays=True (no Nepal public holidays)
    # - show_holidays=True (holidays highlighted in picker)
