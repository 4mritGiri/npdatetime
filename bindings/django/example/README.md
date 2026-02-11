# Example Usage

This directory contains example code demonstrating how to use `django-npdt` in your Django projects.

## Files

- **`models.py`** - Example models using `NepaliDateField` and `NepaliDateTimeField`
- **`forms.py`** - Example forms with `NepaliDatePickerWidget` and various configurations
- **`admin.py`** - Django admin integration examples
- **`views.py`** - Example views using the forms
- **`templates/`** - Example templates using template tags

## Quick Example

### 1. Create a Model

```python
from django.db import models
from npdt.models import NepaliDateField

class Person(models.Model):
    name = models.CharField(max_length=100)
    birth_date_bs = NepaliDateField()
```

### 2. Create a Form

```python
from django import forms
from npdt.widgets import NepaliDatePickerWidget

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'birth_date_bs']
        widgets = {
            'birth_date_bs': NepaliDatePickerWidget(
                mode='BS',
                language='np'
            )
        }
```

### 3. Use in Templates

```django
{% load nepali_date %}

<h2>{{ person.name }}</h2>
<p>Birth Date: {{ person.birth_date_bs|format_nepali_date:"%Y/%m/%d" }}</p>
<p>In AD: {{ person.birth_date_bs|to_gregorian_date:"%B %d, %Y" }}</p>
```

## Running the Example

1. Install django-npdt:
   ```bash
   pip install django-npdt
   ```

2. Add to your INSTALLED_APPS:
   ```python
   INSTALLED_APPS = [
       ...
       'npdt',
       ...
   ]
   ```

3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Create a superuser and test in admin:
   ```bash
   python manage.py createsuperuser
   python manage.py runserver
   ```

Visit `http://localhost:8000/admin/` to see the date picker in action!
