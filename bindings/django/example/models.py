"""Example models using Nepali date fields"""
from django.db import models
from npdatetime_django.models import NepaliDateField, NepaliDateTimeField


class Person(models.Model):
    """Example person model with Nepali date fields"""
    name = models.CharField(max_length=100)
    birth_date_bs = NepaliDateField(
        help_text="Birth date in Bikram Sambat"
    )
    created_at_bs = NepaliDateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} (Born: {self.birth_date_bs})"


class Event(models.Model):
    """Example event model"""
    EVENT_TYPES = [
        ('meeting', 'Meeting'),
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    start_date_bs = NepaliDateField()
    end_date_bs = NepaliDateField(blank=True, null=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['-start_date_bs']
    
    def __str__(self):
        return f"{self.title} ({self.start_date_bs})"
