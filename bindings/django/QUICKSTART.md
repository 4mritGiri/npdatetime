# Quick Start Guide - Django NPDateTime

## Installation

```bash
pip install django-npdt
# or with uv
uv add django-npdt
```

## Setup (3 steps)

### 1. Add to INSTALLED_APPS

```python
# settings.py
INSTALLED_APPS = [
    ...
    'npdt',
    ...
]
```

### 2. Create a Model

```python
# models.py
from django.db import models
from npdt.models import NepaliDateField

class Person(models.Model):
    name = models.CharField(max_length=100)
    birth_date_bs = NepaliDateField()
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Usage

### In Forms

```python
from django import forms
from npdt.widgets import NepaliDatePickerWidget

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'birth_date_bs']
        widgets = {
            'birth_date_bs': NepaliDatePickerWidget(
                mode='BS',      # or 'AD'
                language='np',  # or 'en'
            )
        }
```

### In Templates

```django
{% load nepali_date %}

<h2>{{ person.name }}</h2>
<p>जन्म मिति: {{ person.birth_date_bs|format_nepali_date:"%Y/%m/%d" }}</p>
<p>Fiscal Year: {{ person.birth_date_bs.fiscal_year }}</p>
<p>Date of Birth: {{ person.birth_date_bs|to_gregorian_date:"%B %d, %Y" }}</p>
```

### In Admin

```python
from django.contrib import admin
from .models import Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date_bs']
    # Date picker automatically applied!
```

## Widget Options

```python
NepaliDatePickerWidget(
    mode='BS',                    # 'BS' or 'AD'
    language='en',                # 'en' or 'np'
    theme='auto',                 # 'auto' (follows html[data-theme]), 'light', or 'dark'
    include_time=False,           # Include time picker
    show_today_button=True,       # Show today button
    show_clear_button=True,       # Show clear button
    min_date='2080-01-01',       # Minimum date
    max_date='2085-12-30',       # Maximum date
)
```

## Common Template Filters

```django
{% load nepali_date %}

<!-- Convert to Nepali date -->
{{ gregorian_date|to_nepali_date }}

<!-- Convert to Gregorian date -->
{{ nepali_date|to_gregorian_date }}

<!-- Format Nepali date -->
{{ nepali_date|format_nepali_date:"%Y/%m/%d" }}

<!-- Get month name -->
{{ 1|nepali_month_name:"np" }}  {# बैशाख #}

<!-- Today's date in BS -->
{% nepali_date_today %}

<!-- Fiscal Year and Quarter -->
{{ date|fiscal_year }}     {# 2080/81 #}
{{ date|fiscal_quarter }}  {# 3 #}
```

That's it! You're ready to use Nepali dates in your Django application! 🎉
