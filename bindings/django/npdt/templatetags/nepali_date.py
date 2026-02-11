"""Template tags and filters for Nepali date manipulation"""
from django import template
from django.utils.safestring import mark_safe
import datetime
import json

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
        
    except Exception:
        return ''


@register.filter
def to_gregorian_date(value, format_str='%Y-%m-%d'):
    """
    Convert a Nepali date to Gregorian date.
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
        
    except Exception:
        return ''


@register.filter
def format_nepali_date(value, format_str='%Y-%m-%d'):
    """
    Format a Nepali date string.
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
    """
    return get_nepali_month_name(month_num, language)


@register.filter
def to_nepali_number(value):
    """
    Convert English numerals to Nepali numerals.
    """
    nepali_digits = {
        '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
        '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
    }
    
    result = str(value)
    for eng, nep in nepali_digits.items():
        result = result.replace(eng, nep)
    
    return result


@register.filter
def fiscal_year(value):
    """
    Get the Nepali Fiscal Year.
    """
    if not value or not NPDATETIME_AVAILABLE:
        return ''
    
    try:
        if isinstance(value, str):
            year, month, day = map(int, value.split('-')[:3])
            date = NepaliDate(year, month, day)
        elif isinstance(value, datetime.date):
            date = NepaliDate.from_gregorian(value.year, value.month, value.day)
        elif hasattr(value, 'year') and hasattr(value, 'month') and hasattr(value, 'day'):
            # Potentially already a NepaliDate instance
            date = value
        else:
            return ''
            
        return date.fiscal_year
    except Exception:
        return ''


@register.filter
def fiscal_quarter(value):
    """
    Get the Nepali Fiscal Quarter (1-4).
    """
    if not value or not NPDATETIME_AVAILABLE:
        return ''
    
    try:
        if isinstance(value, str):
            year, month, day = map(int, value.split('-')[:3])
            date = NepaliDate(year, month, day)
        elif isinstance(value, datetime.date):
            date = NepaliDate.from_gregorian(value.year, value.month, value.day)
        elif hasattr(value, 'year') and hasattr(value, 'month') and hasattr(value, 'day'):
            date = value
        else:
            return ''
            
        return date.fiscal_quarter
    except Exception:
        return ''


@register.simple_tag
def nepali_date_today(format_str='%Y-%m-%d'):
    """
    Get today's date in Nepali calendar.
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


@register.inclusion_tag('npdt/widgets/inline_picker.html')
def nepali_date_picker(field_name, value='', mode='BS', language='en', theme='auto', **kwargs):
    """
    Include a Nepali date picker inline in templates.
    """
    options = {
        'mode': mode,
        'language': language,
        'theme': theme,
        **kwargs
    }
    return {
        'field_name': field_name,
        'value': value,
        'mode': mode,
        'language': language,
        'theme': theme,
        'options_json': json.dumps(options)
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
    
    try:
        month_num = int(month_num)
        if not (1 <= month_num <= 12):
            return ''
        
        if language == 'np':
            return months_np[month_num - 1]
        return months_en[month_num - 1]
    except (ValueError, TypeError):
        return ''
