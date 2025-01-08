"""
An inspired library from Python's `datetime` library which will operate on top of
Bikram Sambat (B.S) date. Currently supported B.S date range is 1975 - 2100. Most of the code &
documentation are derived from Python3.5 's datetime.py module & later modified to support
npdatetime.

Supports >= Python3.5
"""

__author__ = "Amrit Giri <amritgiri02595@gmail.com>"

# Importing core components
from .npdate import date
from .datetime import datetime
from .fiscal_year import fiscal_year, get_fiscal_year, get_fiscal_quarter, is_within_fiscal_year, start_of_fiscal_year, end_of_fiscal_year, fiscal_year_range, fiscal_year_report

# Optionally, if you have other utility functions or classes to expose
# from .utils import NepaliNumberConverter


__all__ = [
    "date",
    "datetime",
    "fiscal_year", "get_fiscal_year", "get_fiscal_quarter", "is_within_fiscal_year", "start_of_fiscal_year", "end_of_fiscal_year", "fiscal_year_range", "fiscal_year_report"
]
