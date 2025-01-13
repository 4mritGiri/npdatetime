"""
Functions to calculate and return fiscal year information based on Nepali date.
"""

import json
from datetime import timedelta
from npdatetime.npdate import date


# Custom Fiscal Year Duration: Start month and end month can be set
def fiscal_year(date_obj=None, start_month=4, end_month=3, format=None):
   """
   Return the fiscal year for the provided Nepali date, with a custom fiscal year duration.

   If no date is provided, uses today's date.
   The fiscal year starts on 'start_month' and ends on 'end_month' of the following year.
   """
   if date_obj is None:
      date_obj = date.today()
   return get_fiscal_year(date_obj, start_month, end_month, format)


def get_fiscal_year(date_obj, start_month=4, end_month=3, format=None):
   """
   Return the fiscal year based on the Nepali date object and custom fiscal year duration.

   Supports multiple formats for fiscal year representation.
   """
   start_year, end_year = _determine_fiscal_year(date_obj, start_month)

   if format is None:
      return start_year, end_year

   return _format_fiscal_year(start_year, end_year, format)


def get_fiscal_quarter(date_obj, start_month=4):
   """
   Returns the fiscal quarter based on the Nepali date.

   Parameters:
   - date_obj: Nepali date object with a `month` attribute.
   - start_month: The starting month of the fiscal year (default is 4 for Baishakh).

   Returns:
   - int: The fiscal quarter (1 to 4).
   """
   quarter_length = 3
   fiscal_month = (date_obj.month - start_month + 12) % 12
   return (fiscal_month // quarter_length) + 1


def is_within_fiscal_year(date_obj, fiscal_start_year, start_month=4, end_month=3):
   """
   Check if the given Nepali date is within the fiscal year starting from 'fiscal_start_year'.
   """
   start_date = start_of_fiscal_year(fiscal_start_year, start_month)
   end_date = end_of_fiscal_year(fiscal_start_year, end_month)
   return start_date <= date_obj <= end_date


def start_of_fiscal_year(year, start_month=4):
   """
   Returns the start date of the fiscal year in Nepali date format.
   Fiscal year starts on the 1st of the 'start_month' in the given year.
   """
   return date(year, start_month, 1)


def end_of_fiscal_year(year, end_month=3):
   """
   Returns the end date of the fiscal year in Nepali date format.
   Fiscal year ends on the last day of 'end_month' in the next year.
   """
   return date(year + 1, end_month, date.last_day_of_month(year + 1, end_month))


def fiscal_year_range(start_date, end_date, start_month=4, end_month=3):
   """
   Calculate fiscal years for a given range of Nepali dates.
   Returns a list of fiscal years within the range.
   """
   fiscal_years = []
   current_date = start_date
   while current_date <= end_date:
      fiscal_years.append(fiscal_year(current_date, start_month, end_month))
      current_date += timedelta(days=1)
   return fiscal_years


import json
from calendar import monthrange

def fiscal_year_report(start_date):
   start_year = start_date.year
   start_month = start_date.month
   start_day = start_date.day

   # Fiscal year starts on April 1st and ends on March 30th of the next year
   if start_month < 4:  # If before April, the fiscal year is the previous year
      fiscal_year_start = date(start_year, 4, 1)
      fiscal_year_end = date(start_year + 1, 3, 30)
      fiscal_year = f"{start_year}-{start_year + 1}"
   else:  # If after March, the fiscal year is the current year and the next
      fiscal_year_start = date(start_year + 1, 4, 1)
      fiscal_year_end = date(start_year + 2, 3, 30)
      fiscal_year = f"{start_year + 1}-{start_year + 2}"

   # Determine the quarter based on the start date
   if 4 <= start_month <= 6:
      quarter = 1
   elif 7 <= start_month <= 9:
      quarter = 2
   elif 10 <= start_month <= 12:
      quarter = 3
   else:
      quarter = 4

   # Function to get last day of a month
   def get_last_day_of_month(year, month):
      return monthrange(year, month)[1]

   # Adjust months calculation to handle year wrapping
   def adjust_month_and_year(month_offset):
      month = (fiscal_year_start.month + month_offset - 1) % 12 + 1
      year = fiscal_year_start.year + (fiscal_year_start.month + month_offset - 1) // 12
      return month, year

   # Create quarters with start and end dates
   quarters = {
      "1": [f"{fiscal_year_start.year}-{fiscal_year_start.month:02d}-01", f"{adjust_month_and_year(3)[1]}-{adjust_month_and_year(3)[0]:02d}-{get_last_day_of_month(adjust_month_and_year(3)[1], adjust_month_and_year(3)[0])}"],
      "2": [f"{adjust_month_and_year(4)[1]}-{adjust_month_and_year(4)[0]:02d}-01", f"{adjust_month_and_year(6)[1]}-{adjust_month_and_year(6)[0]:02d}-{get_last_day_of_month(adjust_month_and_year(6)[1], adjust_month_and_year(6)[0])}"],
      "3": [f"{adjust_month_and_year(7)[1]}-{adjust_month_and_year(7)[0]:02d}-01", f"{adjust_month_and_year(9)[1]}-{adjust_month_and_year(9)[0]:02d}-{get_last_day_of_month(adjust_month_and_year(9)[1], adjust_month_and_year(9)[0])}"],
      "4": [f"{adjust_month_and_year(10)[1]}-{adjust_month_and_year(10)[0]:02d}-01", f"{fiscal_year_end.year}-{fiscal_year_end.month:02d}-{fiscal_year_end.day:02d}"],
   }

   result = {
      "fiscal_year": fiscal_year,
      "start_date": str(fiscal_year_start),
      "end_date": str(fiscal_year_end),
      "quarter": quarter,
      "quarters": quarters
   }
   
   return json.dumps(result, ensure_ascii=False, indent=4)



# Private helper functions
def _determine_fiscal_year(date_obj, start_month):
   """
   Determine the fiscal year for a given Nepali date with a custom fiscal year duration.
   """
   if date_obj.month < start_month:  # If the month is before the start month, it's part of the previous fiscal year
      start_year = date_obj.year - 1
   else:
      start_year = date_obj.year
   end_year = start_year + 1
   return start_year, end_year


def _format_fiscal_year(start_year, end_year, format="{start_year}-{end_year}"):
   """
   Format the fiscal year based on user-defined format.
   """
   placeholders = {
      "start_year": start_year,
      "end_year": end_year,
      "start_yyyy": start_year,
      "end_yyyy": end_year,
      "start_yy": str(start_year)[-2:],   # Last two digits of start year
      "end_yy": str(end_year)[-2:],      # Last two digits of end year
      "fiscal_year_name": f"FY {start_year}/{str(end_year)[-2:]}",  # E.g., FY 2080/81
   }

   try:
      return format.format(**placeholders)
   except KeyError as e:
      raise ValueError(f"Unsupported placeholder in format: {e}")
