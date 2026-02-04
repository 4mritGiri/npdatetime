"""Template tags and filters for Nepali date manipulation"""
from django import template
from django.utils.safestring import mark_safe
import datetime

try:
    from npdatetime import NepaliDate
    NPDATETIME_AVAILABLE = True
except ImportError:
    NPDATETIME_AVAILABLE = False

register = template.Library()


@register.filter
def to_nepali_date(value, format_str='%Y-%m-%d'):
    """
    Convert a Gregorian date to Nepali date.
    
    Args:
        value: datetime.date object or string in YYYY-MM-DD format
        format_str: Output format string (default: '%Y-%m-%d')
    
    Returns:
        Formatted Nepali date string or empty string if conversion fails
    
    Example:
        {{ person.birth_date|to_nepali_date }}
        {{ person.birth_date|to_nepali_date:"%Y/%m/%d" }}
    """
    if not value or not NPDATETIME_AVAILABLE:
        return ''
    
    try:
        # Handle datetime.date objects
        if isinstance(value, datetime.date):
            year, month, day = value.year, value.month, value.day
        # Handle string format
        elif isinstance(value, str):
            if '-' in value:
                year, month, day = map(int, value.split('-')[:3])
            else:
                return ''
        else:
            return ''
        
        # Convert to Nepali date
        nepali_date = NepaliDate.from_gregorian(year, month, day)
        
        # Format output
        result = format_str
        result = result.replace('%Y', str(nepali_date.year))
        result = result.replace('%m', f'{nepali_date.month:02d}')
        result = result.replace('%d', f'{nepali_date.day:02d}')
        result = result.replace('%B', get_nepali_month_name(nepali_date.month, 'en'))
        result = result.replace('%b', get_nepali_month_name(nepali_date.month, 'en')[:3])
        
        return result
        
    except Exception as e:
        return ''


@register.filter
def to_gregorian_date(value, format_str='%Y-%m-%d'):
    """
    Convert a Nepali date to Gregorian date.
    
    Args:
        value: Nepali date string in YYYY-MM-DD format
        format_str: Output format string (default: '%Y-%m-%d')
    
    Returns:
        Formatted Gregorian date string or empty string if conversion fails
    
    Example:
        {{ person.birth_date_bs|to_gregorian_date }}
        {{ person.birth_date_bs|to_gregorian_date:"%d/%m/%Y" }}
    """
    if not value or not NPDATETIME_AVAILABLE:
        return ''
    
    try:
        # Parse Nepali date
        if isinstance(value, str):
            year, month, day = map(int, value.split('-'))
        else:
            return ''
        
        # Create NepaliDate and convert
        nepali_date = NepaliDate(year, month, day)
        gy, gm, gd = nepali_date.to_gregorian()
        
        # Create datetime object for formatting
        gregorian_date = datetime.date(gy, gm, gd)
        
        # Use Python's strftime for formatting
        return gregorian_date.strftime(format_str)
        
    except Exception as e:
        return ''


@register.filter
def format_nepali_date(value, format_str='%Y-%m-%d'):
    """
    Format a Nepali date string.
    
    Args:
        value: Nepali date string in YYYY-MM-DD format
        format_str: Output format string
    
    Returns:
        Formatted date string
    
    Example:
        {{ date_bs|format_nepali_date:"%Y/%m/%d" }}
    """
    if not value:
        return ''
    
    try:
        year, month, day = map(int, value.split('-'))
        
        result = format_str
        result = result.replace('%Y', str(year))
        result = result.replace('%m', f'{month:02d}')
        result = result.replace('%d', f'{day:02d}')
        result = result.replace('%B', get_nepali_month_name(month, 'en'))
        result = result.replace('%b', get_nepali_month_name(month, 'en')[:3])
        
        return result
        
    except Exception:
        return value


@register.filter
def nepali_month_name(month_num, language='en'):
    """
    Get Nepali month name.
    
    Args:
        month_num: Month number (1-12)
        language: 'en' or 'np'
    
    Returns:
        Month name string
    
    Example:
        {{ 1|nepali_month_name }}  # Returns "Baisakh"
        {{ 1|nepali_month_name:"np" }}  # Returns "बैशाख"
    """
    return get_nepali_month_name(month_num, language)


@register.filter
def to_nepali_number(value):
    """
    Convert English numerals to Nepali numerals.
    
    Args:
        value: Number or string containing numbers
    
    Returns:
        String with Nepali numerals
    
    Example:
        {{ 2081|to_nepali_number }}  # Returns "२०८१"
    """
    nepali_digits = {
        '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
        '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
    }
    
    result = str(value)
    for eng, nep in nepali_digits.items():
        result = result.replace(eng, nep)
    
    return result


@register.simple_tag
def nepali_date_today(format_str='%Y-%m-%d'):
    """
    Get today's date in Nepali calendar.
    
    Args:
        format_str: Output format string
    
    Returns:
        Formatted today's Nepali date
    
    Example:
        {% nepali_date_today %}
        {% nepali_date_today "%Y/%m/%d" %}
    """
    if not NPDATETIME_AVAILABLE:
        return ''
    
    try:
        today = NepaliDate.today()
        
        result = format_str
        result = result.replace('%Y', str(today.year))
        result = result.replace('%m', f'{today.month:02d}')
        result = result.replace('%d', f'{today.day:02d}')
        result = result.replace('%B', get_nepali_month_name(today.month, 'en'))
        result = result.replace('%b', get_nepali_month_name(today.month, 'en')[:3])
        
        return result
        
    except Exception:
        return ''


@register.inclusion_tag('npdatetime_django/widgets/inline_picker.html')
def nepali_date_picker(field_name, value='', mode='BS', language='en', **kwargs):
    """
    Include a Nepali date picker inline in templates.
    
    Args:
        field_name: Name of the input field
        value: Initial value
        mode: 'BS' or 'AD'
        language: 'en' or 'np'
        **kwargs: Additional options
    
    Example:
        {% nepali_date_picker "birth_date" mode="BS" language="np" %}
    """
    return {
        'field_name': field_name,
        'value': value,
        'mode': mode,
        'language': language,
        'options': kwargs
    }


# Helper function
def get_nepali_month_name(month_num, language='en'):
    """Get the name of a Nepali month."""
    months_en = [
        'Baisakh', 'Jestha', 'Ashadh', 'Shrawan', 'Bhadra', 'Ashwin',
        'Kartik', 'Mangshir', 'Poush', 'Magh', 'Falgun', 'Chaitra'
    ]
    
    months_np = [
        'बैशाख', 'जेठ', 'असार', 'साउन', 'भदौ', 'असोज',
        'कात्तिक', 'मंसिर', 'पुस', 'माघ', 'फागुन', 'चैत'
    ]
    
    if not (1 <= month_num <= 12):
        return ''
    
    if language == 'np':
        return months_np[month_num - 1]
    return months_en[month_num - 1]
