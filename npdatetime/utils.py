
def get_fiscal_year_by_date(date_obj):
   """Return fiscal year by the given Nepali datetime object"""
   # Fiscal year starts in Shrawan (month 4)
   if date_obj.month < 4:  # Months 1, 2, 3 are part of the previous fiscal year
      fiscal_year = (date_obj.year - 1, date_obj.year)
   else:
      fiscal_year = (date_obj.year, date_obj.year + 1)
   return fiscal_year
