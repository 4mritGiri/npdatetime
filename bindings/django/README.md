# Django NPDateTime

**Nepali Date Field and Date Picker Widget for Django**

A Django package that provides custom model fields, form fields, and a modern date picker widget for working with Nepali (Bikram Sambat) dates. Powered by the high-performance [npdatetime](https://github.com/4mritGiri/npdatetime) library.

## Features

✨ **Custom Model Fields** - `NepaliDateField` and `NepaliDateTimeField` with direct access to fiscal year/quarter properties

✨ **Fiscal Year Support** - Built-in support for Nepali Fiscal Years (e.g., 2080/81) and quarters

🎨 **Beautiful Date Picker Widget** - Modern, responsive date picker with both BS and AD modes

🌐 **Bilingual Support** - English and Nepali language options

🔄 **Auto Conversion** - Seamless conversion between Bikram Sambat and Gregorian calendars

📝 **Template Tags & Filters** - Rich template tags for date formatting and conversion

⚡ **High Performance** - Built on Rust for maximum speed

🎯 **Django Integration** - Works seamlessly with Django's forms and admin

🔒 **Enterprise Options** - Disable past dates, weekends, holidays, specific dates/weekdays, and custom validation callbacks

## For Developers

If you're contributing to this package, the JavaScript/CSS files are synchronized from `../javascript/`. When you update the date picker:

```bash
# Run the build script to sync assets
python build_assets.py
# or
./build_assets.sh
```

This copies:
- `picker.js` → `static/npdt/js/picker.min.js`
- `picker.css` → `static/npdt/css/picker.css`
- `pkg/` → `static/npdt/js/pkg/`

## Installation

```bash
pip install django-npdt
# or with uv
uv add django-npdt
```

## Quick Start

### 1. Add to INSTALLED_APPS

```python
# settings.py
INSTALLED_APPS = [
    ...
    'npdt',
    ...
]
```

### 2. Use in Models

```python
from django.db import models
from npdt import NepaliDateField

class Person(models.Model):
    name = models.CharField(max_length=100)
    birth_date_bs = NepaliDateField()
    
    def __str__(self):
        return f"{self.name} - {self.birth_date_bs}"
```

### 3. Use in Forms

```python
from django import forms
from npdt import NepaliDateField, NepaliDatePickerWidget

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
from npdt.models import NepaliDateField

class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_date_bs = NepaliDateField(mode='BS', language='np')  # Configurable!
```

#### NepaliDateTimeField

Stores Nepali dates with time in `YYYY-MM-DD HH:MM:SS` format.

```python
from npdt.models import NepaliDateTimeField

class Meeting(models.Model):
    title = models.CharField(max_length=200)
    scheduled_at_bs = NepaliDateTimeField()
```

### Form Fields and Widgets

#### Basic Date Picker

```python
from npdt.forms import NepaliDateField

class PersonForm(forms.Form):
    birth_date = NepaliDateField(
        mode='BS',           # 'BS' or 'AD'
        language='en',       # 'en' or 'np'
    )
```

#### Advanced Configuration

```python
from npdt.widgets import NepaliDatePickerWidget

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

#### Enterprise Configuration

```python
from npdt.widgets import NepaliDatePickerWidget

class LeaveForm(forms.Form):
    # Future dates only, no weekends or holidays
    leave_date = forms.CharField(
        widget=NepaliDatePickerWidget(
            mode='BS',
            disable_past_dates=True,
            disable_weekends=True,
            disable_holidays=True,
        )
    )
```

#### Using `widget_kwargs` with Form Fields

`NepaliDateField` and `NepaliDateRangeField` accept `widget_kwargs` to pass options through to the widget:

```python
from npdt.forms import NepaliDateField

class LeaveForm(forms.Form):
    start_date = NepaliDateField(
        mode='BS',
        widget_kwargs={
            'disable_past_dates': True,
            'disable_holidays': True,
            'disable_weekends': True,
            'show_tithi': True,
        }
    )
```

#### Date Range Picker

```python
from npdt.forms import NepaliDateRangeField

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

#### Inline Date Picker

```django
{% load nepali_date %}

{# Basic #}
{% nepali_date_picker "event_date" %}

{# With dynamic options #}
{% nepali_date_picker "event_date" disable_past_dates=True %}
{% nepali_date_picker "event_date" disable_weekends=True disable_holidays=True %}
{% nepali_date_picker "event_date" admin_theme=True %}
{% nepali_date_picker "event_date" show_tithi=True %}
```

### Widget Options

The `NepaliDatePickerWidget` accepts the following options:

#### Core Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | str | `'BS'` | Calendar mode: `'BS'` or `'AD'` |
| `language` | str | `'en'` | Interface language: `'en'` or `'np'` |
| `theme` | str | `'auto'` | Color theme: `'auto'`, `'light'`, `'dark'`, or `'admin'` |
| `format` | str | `'%Y-%m-%d'` | Date format string |
| `include_time` | bool | `False` | Include time picker |
| `show_today_button` | bool | `True` | Show "Today" button |
| `show_clear_button` | bool | `True` | Show "Clear" button |
| `min_date` | str | `None` | Minimum selectable date (YYYY-MM-DD) |
| `max_date` | str | `None` | Maximum selectable date (YYYY-MM-DD) |

#### Dynamic Disabling Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `disabled_dates` | list[str] | `[]` | List of date strings to disable (YYYY-MM-DD) |
| `disabled_days` | list[int] \| str | `[]` | Weekday indices to disable. Supports: list `[0,6]`, range `"1-5"` (Mon–Fri), mixed `"1-5,0"`. 0=Sunday, 1=Monday, ..., 6=Saturday |
| `disable_past_dates` | bool | `False` | Disable all dates before today |
| `disable_weekends` | bool | `False` | Disable weekends (Saturday in BS, Sunday in AD) |
| `disable_holidays` | bool | `False` | Disable holidays from the holiday provider |
| `show_holidays` | bool | `True` | Highlight holidays visually (without disabling) |
| `holiday_provider` | HolidayProvider | `None` | Custom holiday provider. Defaults to `NepalPublicHolidays` when `disable_holidays=True` |
| `on_date_disabled` | str | `'prevent'` | Behavior when a disabled date is selected: `'prevent'` or `'warn'` |
| `show_tithi` | bool | `False` | Show lunar tithi on date hover |
| `admin_theme` | bool | `False` | Shortcut for `theme='admin'` — matches Django admin styling |

### Holiday Provider System

The widget includes an extensible holiday provider system for defining which dates should be treated as holidays.

#### Built-in: NepalPublicHolidays

Covers major Nepal public holidays for BS years 2070–2100. Automatically used when `disable_holidays=True` and no custom provider is specified.

```python
from npdt.widgets import NepaliDatePickerWidget

widget = NepaliDatePickerWidget(
    disable_holidays=True,  # Uses NepalPublicHolidays by default
)
```

#### Custom Holiday Provider

Subclass `HolidayProvider` to define your organization's holidays:

```python
from npdt.holidays import HolidayProvider, HolidayDate

class MyCompanyHolidays(HolidayProvider):
    def get_holidays(self, year, month=None):
        return [
            HolidayDate('2082-01-01', 'Company Foundation Day', name_np='कम्पनी स्थापना दिवस'),
            HolidayDate('2082-06-15', 'Annual Retreat', type='optional'),
        ]

widget = NepaliDatePickerWidget(
    holiday_provider=MyCompanyHolidays(),
    disable_holidays=True,
)
```

#### CompositeHolidayProvider

Merge multiple providers (e.g., public holidays + company holidays):

```python
from npdt.holidays import CompositeHolidayProvider, NepalPublicHolidays

provider = CompositeHolidayProvider(
    NepalPublicHolidays(),
    MyCompanyHolidays(),
)

widget = NepaliDatePickerWidget(
    holiday_provider=provider,
    disable_holidays=True,
    show_holidays=True,
)
```

#### StaticHolidayProvider

Quick one-off configuration without writing a full class:

```python
from npdt.holidays import StaticHolidayProvider

provider = StaticHolidayProvider(
    ['2082-01-01', '2082-09-03'],
    name='Bank Holiday',
)

widget = NepaliDatePickerWidget(
    holiday_provider=provider,
    disable_holidays=True,
)
```

### Django Admin Integration

The date picker automatically integrates with Django admin. Use `admin_theme=True` to match Django admin's styling:

```python
from django.contrib import admin
from npdt.widgets import NepaliDatePickerWidget

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date_bs']
    fields = ['name', 'birth_date_bs']
```

For explicit admin theme on individual widgets:

```python
class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'birth_date_bs']
        widgets = {
            'birth_date_bs': NepaliDatePickerWidget(
                admin_theme=True,
                disable_holidays=True,
            ),
        }
```

## Examples

### Complete Model Example

```python
from django.db import models
from npdt.models import NepaliDateField, NepaliDateTimeField

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
from npdt.widgets import NepaliDatePickerWidget
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

### Production Example: Banking Form

```python
from django import forms
from npdt.widgets import NepaliDatePickerWidget

class FacilityForm(forms.ModelForm):
    class Meta:
        model = CustomerFacility
        fields = ['reference', 'initiated_date', 'approval_date']
        widgets = {
            'initiated_date': NepaliDatePickerWidget(
                mode='AD',
                disable_holidays=True,
            ),
            'approval_date': NepaliDatePickerWidget(
                disable_holidays=True,
            ),
        }
```

### Converting BS ↔ AD in Forms

When storing AD dates in the database but displaying BS in the picker:

```python
from django import forms
from npdt.widgets import NepaliDatePickerWidget

class MyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convert AD dates to BS for initial display
        for date_field in ('initiated_date', 'approval_date'):
            if date_field in self.fields and self.initial.get(date_field):
                try:
                    from npdatetime import NepaliDate
                    ad_val = self.initial[date_field]
                    if hasattr(ad_val, 'year'):
                        np_date = NepaliDate.from_gregorian(
                            ad_val.year, ad_val.month, ad_val.day
                        )
                        self.initial[date_field] = str(np_date)
                except Exception:
                    pass

    def _clean_bs_date(self, field_name):
        """Convert BS date string from picker to AD date for the model."""
        value = self.cleaned_data.get(field_name)
        if not value:
            return value
        if hasattr(value, 'year') and not isinstance(value, str):
            return value
        try:
            from npdatetime import NepaliDate
            import datetime
            parts = [int(p) for p in str(value).split('-')]
            np_date = NepaliDate(parts[0], parts[1], parts[2])
            gy, gm, gd = np_date.to_gregorian()
            return datetime.date(gy, gm, gd)
        except Exception:
            raise forms.ValidationError(f'Invalid BS date format for {field_name}.')

    def clean_initiated_date(self):
        return self._clean_bs_date('initiated_date')
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
- [npdatetime(Rust)](https://github.com/4mritGiri/npdatetime) - High-performance Nepali datetime library (Rust)

## Support

For bugs and feature requests, please open an issue on [GitHub](https://github.com/4mritGiri/npdatetime/issues).
