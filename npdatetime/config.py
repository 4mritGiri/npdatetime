import os

# Define the base directory
BASE_DIR = os.path.dirname(__file__)

# Path to the calendar data file
CALENDAR_PATH = os.path.join(BASE_DIR, 'data', 'calendar_bs.csv')

# Reference date for conversions
REFERENCE_DATE_AD = {'year': 1918, 'month': 4, 'day': 13}

# Valid range for Nepali dates
MINDATE = {'year': 1975, 'month': 1, 'day': 1}
MAXDATE = {'year': 2100, 'month': 12, 'day': 30}
