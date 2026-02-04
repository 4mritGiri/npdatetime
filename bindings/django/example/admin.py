"""Admin configuration for example models"""
from django.contrib import admin
from .models import Person, Event


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Admin interface for Person model"""
    list_display = ['name', 'birth_date_bs', 'created_at_bs']
    list_filter = ['birth_date_bs']
    search_fields = ['name']
    fields = ['name', 'birth_date_bs']
    
    # The NepaliDatePickerWidget will be automatically used
    # because the model field defines it in formfield()


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for Event model"""
    list_display = ['title', 'event_type', 'start_date_bs', 'end_date_bs']
    list_filter = ['event_type', 'start_date_bs']
    search_fields = ['title', 'description']
    date_hierarchy = 'start_date_bs'  # Note: This uses the BS date field
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'event_type', 'description')
        }),
        ('Dates', {
            'fields': ('start_date_bs', 'end_date_bs'),
            'description': 'Enter dates in Bikram Sambat calendar'
        }),
    )
