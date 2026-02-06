# Django NPDateTime

**Nepali Date Field and Date Picker Widget for Django**

A Django package that provides custom model fields, form fields, and a modern date picker widget for working with Nepali (Bikram Sambat) dates. Powered by the high-performance [npdatetime-rust](https://github.com/4mritGiri/npdatetime-rust) library.

## Features

✨ **Custom Model Fields** - `NepaliDateField` and `NepaliDateTimeField` with direct access to fiscal year/quarter properties
...
✨ **Fiscal Year Support** - Built-in support for Nepali Fiscal Years (e.g., 2080/81) and quarters

🎨 **Beautiful Date Picker Widget** - Modern, responsive date picker with both BS and AD modes

🌐 **Bilingual Support** - English and Nepali language options

🔄 **Auto Conversion** - Seamless conversion between Bikram Sambat and Gregorian calendars

📝 **Template Tags & Filters** - Rich template tags for date formatting and conversion

⚡ **High Performance** - Built on Rust for maximum speed

🎯 **Django Integration** - Works seamlessly with Django's forms and admin

## For Developers

If you're contributing to this package, the JavaScript/CSS files are synchronized from `../javascript/`. When you update the date picker:

```bash
# Run the build script to sync assets
python build_assets.py
# or
./build_assets.sh
```

This copies:
- `date_picker.js` → `static/npdatetime_django/js/date_picker.min.js`
- `date_picker.css` → `static/npdatetime_django/css/date_picker.css`
- `pkg/` → `static/npdatetime_django/js/pkg/`

## Installation

```bash
pip install django-npdatetime
```

## Quick Start

### 1. Add to INSTALLED_APPS

```python
# settings.py
INSTALLED_APPS = [
    ...
    'npdatetime_django',
    ...
]
```

### 2. Use in Models

```python
from django.db import models
from npdatetime_django import NepaliDateField

class Person(models.Model):
    name = models.CharField(max_length=100)
    birth_date_bs = NepaliDateField()
    
    def __str__(self):
        return f"{self.name} - {self.birth_date_bs}"
```

### 3. Use in Forms

```python
from django import forms
from npdatetime_django import NepaliDateField, NepaliDatePickerWidget

class PersonForm(forms.Form):
    name = forms.CharField(max_length=100)
    birth_date = NepaliDateField(
        mode='BS',
        language='np',
        label='जन्म मिति'
    )
```

### 4. Use Template Tags

```django
{% load nepali_date %}

<p>Birth Date (BS): {{ person.birth_date_bs }}</p>
<p>Birth Date (AD): {{ person.birth_date_bs|to_gregorian_date }}</p>
<p>Fiscal Year: {{ person.birth_date_bs.fiscal_year }}</p>
<p>Today in BS: {% nepali_date_today %}</p>
<p>Month: {{ 1|nepali_month_name:"np" }}</p>
<p>Inline Picker: {% nepali_date_picker "event_date" theme="dark" %}</p>
```

## Usage Guide

### Model Fields

#### NepaliDateField

Stores Nepali dates in `YYYY-MM-DD` format.

```python
from npdatetime_django.models import NepaliDateField

class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_date_bs = NepaliDateField(mode='BS', language='np')  # Configurable!
```

#### NepaliDateTimeField

Stores Nepali dates with time in `YYYY-MM-DD HH:MM:SS` format.

```python
from npdatetime_django.models import NepaliDateTimeField

class Meeting(models.Model):
    title = models.CharField(max_length=200)
    scheduled_at_bs = NepaliDateTimeField()
```

### Form Fields and Widgets

#### Basic Date Picker

```python
from npdatetime_django.forms import NepaliDateField

class PersonForm(forms.Form):
    birth_date = NepaliDateField(
        mode='BS',           # 'BS' or 'AD'
        language='en',       # 'en' or 'np'
    )
```

#### Advanced Configuration

```python
from npdatetime_django.widgets import NepaliDatePickerWidget

class EventForm(forms.Form):
    event_date = forms.CharField(
        widget=NepaliDatePickerWidget(
            mode='BS',
            language='np',
            theme='dark',
            show_today_button=True,
            show_clear_button=True,
            min_date='2080-01-01',
            max_date='2085-12-30',
        )
    )
```

#### Date Range Picker

```python
from npdatetime_django.forms import NepaliDateRangeField

class ReportForm(forms.Form):
    report_period = NepaliDateRangeField(
        mode='BS',
        language='np'
    )
    
    def clean_report_period(self):
        period = self.cleaned_data['report_period']
        start_date, end_date = period.split(' to ')
        # Process date range
        return period
```

### Template Tags and Filters

Load the template tag library:

```django
{% load nepali_date %}
```

#### Convert Gregorian to Nepali

```django
{{ gregorian_date|to_nepali_date }}
{{ gregorian_date|to_nepali_date:"%Y/%m/%d" }}
```

#### Convert Nepali to Gregorian

```django
{{ nepali_date|to_gregorian_date }}
{{ nepali_date|to_gregorian_date:"%d/%m/%Y" }}
```

#### Format Nepali Date

```django
{{ "2081-01-15"|format_nepali_date:"%Y/%m/%d" }}
```

#### Get Month Name

```django
{{ 1|nepali_month_name }}        {# Baisakh #}
{{ 1|nepali_month_name:"np" }}   {# बैशाख #}
```

#### Convert to Nepali Numerals

```django
{{ 2081|to_nepali_number }}  {# २०८१ #}
```

#### Fiscal Year and Quarter

```django
{{ "2081-01-15"|fiscal_year }}     {# 2080/81 #}
{{ "2081-01-15"|fiscal_quarter }}  {# 3 #}
```

#### Get Today's Date

```django
{% nepali_date_today %}
{% nepali_date_today "%Y/%m/%d" %}
```

### Widget Options

The `NepaliDatePickerWidget` accepts the following options:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | str | `'BS'` | Calendar mode: `'BS'` or `'AD'` |
| `language` | str | `'en'` | Interface language: `'en'` or `'np'` |
| `theme` | str | `'auto'` | Color theme: `'auto'`, `'light'`, or `'dark'`. `'auto'` follows `html[data-theme]`. |
| `format` | str | `'%Y-%m-%d'` | Date format string |
| `include_time` | bool | `False` | Include time picker |
| `show_today_button` | bool | `True` | Show "Today" button |
| `show_clear_button` | bool | `True` | Show "Clear" button |
| `min_date` | str | `None` | Minimum selectable date |
| `max_date` | str | `None` | Maximum selectable date |

## Admin Integration

The date picker automatically integrates with Django admin:

```python
from django.contrib import admin
from .models import Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date_bs']
    fields = ['name', 'birth_date_bs']
```

## Examples

### Complete Model Example

```python
from django.db import models
from npdatetime_django.models import NepaliDateField, NepaliDateTimeField

class Employee(models.Model):
    name = models.CharField(max_length=100)
    join_date_bs = NepaliDateField(help_text="Joining date in BS")
    birth_date_bs = NepaliDateField(blank=True, null=True)
    last_login_bs = NepaliDateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-join_date_bs']
    
    def __str__(self):
        return f"{self.name} (Joined: {self.join_date_bs})"
```

### ModelForm Example

```python
from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'join_date_bs', 'birth_date_bs']
        widgets = {
            'join_date_bs': NepaliDatePickerWidget(
                mode='BS',
                language='np',
                theme='light'
            ),
            'birth_date_bs': NepaliDatePickerWidget(
                mode='BS',
                language='np'
            ),
        }
```

### Template Example

```django
{% load nepali_date %}
<!DOCTYPE html>
<html>
<head>
    <title>Employee Details</title>
</head>
<body>
    <h1>{{ employee.name }}</h1>
    
    <div>
        <strong>Join Date (BS):</strong> 
        {{ employee.join_date_bs|format_nepali_date:"%Y/%m/%d" }}
    </div>
    
    <div>
        <strong>Join Date (AD):</strong> 
        {{ employee.join_date_bs|to_gregorian_date:"%B %d, %Y" }}
    </div>
    
    <div>
        <strong>Birth Month:</strong>
        {{ employee.birth_date_bs|slice:":7"|last|int|nepali_month_name:"np" }}
    </div>
</body>
</html>
```

## Requirements

- Python >= 3.8
- Django >= 3.2
- npdatetime >= 0.1.0

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Credits

Built on top of:
- [npdatetime-rust](https://github.com/4mritGiri/npdatetime-rust) - High-performance Nepali datetime library

## Support

For bugs and feature requests, please open an issue on [GitHub](https://github.com/4mritGiri/npdatetime-rust/issues).
