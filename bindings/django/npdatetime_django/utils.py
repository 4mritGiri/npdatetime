"""Utility functions for working with Nepali dates in Django"""

try:
    from npdatetime import NepaliDate
    NPDATETIME_AVAILABLE = True
except ImportError:
    NPDATETIME_AVAILABLE = False


def convert_bs_to_ad(bs_date_str):
    """
    Convert a Nepali (BS) date string to Gregorian (AD) date.
    
    Args:
        bs_date_str (str): Date in format "YYYY-MM-DD"
    
    Returns:
        str: Gregorian date in format "YYYY-MM-DD" or None if conversion fails
    
    Example:
        >>> convert_bs_to_ad("2081-01-15")
        "2024-05-02"
    """
    if not bs_date_str or not NPDATETIME_AVAILABLE:
        return None
    
    try:
        year, month, day = map(int, bs_date_str.split('-'))
        nepali_date = NepaliDate(year, month, day)
        gy, gm, gd = nepali_date.to_gregorian()
        return f"{gy}-{gm:02d}-{gd:02d}"
    except Exception:
        return None


def convert_ad_to_bs(ad_date_str):
    """
    Convert a Gregorian (AD) date string to Nepali (BS) date.
    
    Args:
        ad_date_str (str): Date in format "YYYY-MM-DD"
    
    Returns:
        str: Nepali date in format "YYYY-MM-DD" or None if conversion fails
    
    Example:
        >>> convert_ad_to_bs("2024-05-02")
        "2081-01-15"
    """
    if not ad_date_str or not NPDATETIME_AVAILABLE:
        return None
    
    try:
        year, month, day = map(int, ad_date_str.split('-'))
        nepali_date = NepaliDate.from_gregorian(year, month, day)
        return f"{nepali_date.year}-{nepali_date.month:02d}-{nepali_date.day:02d}"
    except Exception:
        return None


def get_nepali_month_names(language='en'):
    """
    Get list of Nepali month names.
    
    Args:
        language (str): 'en' for English or 'np' for Nepali
    
    Returns:
        list: List of month names
    """
    months_en = [
        'Baisakh', 'Jestha', 'Ashadh', 'Shrawan', 'Bhadra', 'Ashwin',
        'Kartik', 'Mangshir', 'Poush', 'Magh', 'Falgun', 'Chaitra'
    ]
    
    months_np = [
        'बैशाख', 'जेठ', 'असार', 'साउन', 'भदौ', 'असोज',
        'कात्तिक', 'मंसिर', 'पुस', 'माघ', 'फागुन', 'चैत'
    ]
    
    return months_np if language == 'np' else months_en


def validate_nepali_date(date_str):
    """
    Validate a Nepali date string.
    
    Args:
        date_str (str): Date string to validate
    
    Returns:
        tuple: (is_valid, error_message)
    
    Example:
        >>> validate_nepali_date("2081-01-15")
        (True, None)
        >>> validate_nepali_date("2081-13-01")
        (False, "Month must be between 1 and 12")
    """
    if not date_str:
        return False, "Date string is empty"
    
    try:
        parts = date_str.split('-')
        if len(parts) != 3:
            return False, "Invalid date format. Use YYYY-MM-DD"
        
        year, month, day = map(int, parts)
        
        if year < 1975 or year > 2100:
            return False, "Year must be between 1975 and 2100"
        
        if month < 1 or month > 12:
            return False, "Month must be between 1 and 12"
        
        if day < 1 or day > 32:
            return False, "Day must be between 1 and 32"
        
        # Validate with npdatetime if available
        if NPDATETIME_AVAILABLE:
            try:
                NepaliDate(year, month, day)
            except Exception as e:
                return False, str(e)
        
        return True, None
        
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD with numeric values"
    except Exception as e:
        return False, str(e)
