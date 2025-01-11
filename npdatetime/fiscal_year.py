"""
Functions to calculate and return fiscal year information based on Nepali date.
"""
from datetime import timedelta
from npdatetime.npdate import date
import json


# Custom Fiscal Year Duration: Start month and end month can be set
def fiscal_year(date_obj=None, start_month=4, end_month=3, format=None):
   """
   Return the fiscal year for the provided Nepali date, with a custom fiscal year duration.
   
   If no date is provided, uses today's date.
   The fiscal year starts on 'start_month' and ends on 'end_month' of the following year.
   """
   # from npdatetime import date
   if date_obj is None:
      date_obj = date.today()
   return get_fiscal_year(date_obj, start_month, end_month, format)


def get_fiscal_year(date_obj, start_month=4, end_month=3, format=None):
   """
   Return the fiscal year based on the Nepali date object and custom fiscal year duration.
   
   Supports multiple formats for fiscal year representation.
   """
   start_year, end_year = _determine_fiscal_year(date_obj, start_month, end_month)

   if format is None:
      return (start_year, end_year)

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
   # Ensure the months wrap around the year
   quarter_mapping = {
      1: [(start_month + i - 1) % 12 or 12 for i in range(3)],  # Q1
      2: [(start_month + i - 1) % 12 or 12 for i in range(3, 6)],  # Q2
      3: [(start_month + i - 1) % 12 or 12 for i in range(6, 9)],  # Q3
      4: [(start_month + i - 1) % 12 or 12 for i in range(9, 12)],  # Q4
   }

   for quarter, months in quarter_mapping.items():
      if date_obj.month in months:
         return quarter

   # If no match is found, raise an error (shouldn't occur with valid input)
   raise ValueError(f"Invalid month {date_obj.month} in the date object.")


def is_within_fiscal_year(date_obj, fiscal_start_year):
   """
   Check if the given Nepali date is within the fiscal year starting from 'fiscal_start_year'.
   """
   start_date = start_of_fiscal_year(fiscal_start_year)
   end_date = end_of_fiscal_year(fiscal_start_year)
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
   Fiscal year ends on the last day of 'end_month' in the given year.
   """
   # from npdatetime import date
   if end_month == 2:  # Handle leap year for February if required (Assuming end of Ashad is fixed)
      # Leap year correction for Nepali calendar (can be extended to more months if needed)
      end_date = date(year + 1, end_month, 30)
   else:
      end_date = date(year + 1, end_month, 30)
   return end_date

def fiscal_year_range(start_date, end_date, start_month=4, end_month=3):
   """
   Calculate fiscal years for a given range of Nepali dates.
   Returns a list of fiscal years within the range.
   """
   fiscal_years = []
   current_date = start_date
   while current_date <= end_date:
      fiscal_years.append(fiscal_year(current_date, start_month, end_month))
      current_date = current_date + timedelta(days=1)  # Move to next date
   return fiscal_years


def fiscal_year_report(date_obj, start_month=4, end_month=3):
   """
   Return fiscal year report for the given date.
   Includes fiscal year, quarters, and weeks in a structured JSON format.
   """
   start_year, end_year = _determine_fiscal_year(date_obj, start_month, end_month)
   fiscal_quarter = get_fiscal_quarter(date_obj, start_month)
   fiscal_start_date = start_of_fiscal_year(start_year, start_month)
   fiscal_end_date = end_of_fiscal_year(end_year, end_month)
   
   report = {
      "fiscal_year": f"{start_year}-{end_year}",
      "start_date": fiscal_start_date.isoformat(),
      "end_date": fiscal_end_date.isoformat(),
      "quarter": fiscal_quarter,
      "quarters": {
         1: [fiscal_start_date.isoformat(), (fiscal_start_date + timedelta(days=90)).isoformat()],
         2: [(fiscal_start_date + timedelta(days=91)).isoformat(), (fiscal_start_date + timedelta(days=180)).isoformat()],
         3: [(fiscal_start_date + timedelta(days=181)).isoformat(), (fiscal_start_date + timedelta(days=270)).isoformat()],
         4: [(fiscal_start_date + timedelta(days=271)).isoformat(), fiscal_end_date.isoformat()],
      }
   }
   return json.dumps(report, indent=4)


# Private helper functions
def _determine_fiscal_year(date_obj, start_month, end_month):
   """
   Determine the fiscal year for a given Nepali date with a custom fiscal year duration.
   If the date is before 'start_month', it's part of the previous fiscal year.
   """
   if date_obj.month < start_month:  # If the month is before the start month, it's part of the previous fiscal year
      start_year = date_obj.year - 1
      end_year = date_obj.year
   else:
      start_year = date_obj.year
      end_year = date_obj.year + 1
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
      "end_yy": str(end_year)[-2:],       # Last two digits of end year
      "start_yyy": str(start_year)[-3:],  # Last three digits of start year
      "end_yyy": str(end_year)[-3:],      # Last three digits of end year
      "fiscal_year_name": f"FY {start_year}/{str(end_year)[-2:]}",  # E.g., FY 2080/81
   }

   try:
      return format.format(**placeholders)
   except KeyError as e:
      raise ValueError(f"Unsupported placeholder in format: {e}")
