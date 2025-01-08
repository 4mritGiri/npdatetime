# **Nepali Datetime (Bikram Sambat Date & Nepal Time)**  

[![PyPI version](https://badge.fury.io/py/npdatetime.svg)](https://badge.fury.io/py/npdatetime)
<!-- [![CI status](https://github.com/opensource-npdatetime/py-npdatetime/actions/workflows/python-package.yml/badge.svg?branch=??)](https://github.com/opensource-nepnpdatetimeal/py-npdatetime/actions)
[![Downloads](https://img.shields.io/pypi/dm/npdatetime.svg?maxAge=180)](https://pypi.org/project/npdatetime/)
[![codecov](https://codecov.io/gh/opensource-npdatetime/py-npdatetime/branch/main/graph/badge.svg?token=PTUHYWCJ4I)](https://codecov.io/gh/opensource-npdatetime/py-npdatetime) -->


A Python library inspired by Python's core `datetime` module, designed specifically for operations based on the **Bikram Sambat (B.S.)** calendar and **Nepal Time (NPT)** timezone (`UTC+05:45`).  

This library bridges the gap between traditional Nepali dates and modern software development, allowing developers to handle Nepali dates with ease while maintaining compatibility with Python's `datetime`.  

---

## **Key Features**  

- Full support for Bikram Sambat (B.S.) date operations.  
- Handles Nepal Time (NPT) seamlessly (`UTC+05:45`).  
- Built-in compatibility with Python's `datetime` module.  
- Supports date formatting with Nepali Unicode for localized output.  
- Conversion between Bikram Sambat and Gregorian calendars.  
- Convenient utilities for date parsing, arithmetic, and calendars.  
- Compatible with Python 3.5 and above.  

---

## **Installation**  

Install the package via `pip`:  
```bash  
pip install npdatetime  
```  

---

## **Quick Start**  

Here's how you can use `npdatetime` alongside Python's standard `datetime` module:  

### **Importing**  
```python  
import datetime  
import npdatetime  
```  

### **Getting Today's Date**  
```python  
# Gregorian date  
datetime.date.today()  

# Bikram Sambat date  
npdatetime.date.today()  
```  

### **Current Date and Time**  
```python  
# Gregorian datetime  
datetime.datetime.now()  

# Bikram Sambat datetime  
npdatetime.datetime.now()  
```  

---

## **Key Functionalities**  

### **Creating Date and Datetime Objects**  
```python  
# Gregorian date  
datetime.date(2020, 9, 4)  

# Bikram Sambat date  
npdatetime.date(2077, 5, 19)  

# Gregorian datetime  
datetime.datetime(2020, 9, 4, 8, 26, 10, 123456)  

# Bikram Sambat datetime  
npdatetime.datetime(2077, 5, 19, 8, 26, 10, 123456)  
```  

### **Date Formatting with Localization**  
```python  
# Formatting a Bikram Sambat date  
npdatetime.datetime(2077, 5, 19).strftime("%d %B %Y")  
# Output: 19 Bhadau 2077  

# Formatting with Nepali Unicode  
npdatetime.date(2077, 10, 25).strftime('%K-%n-%D (%k %N %G)')  
# Output: २०७७-१०-२५ (२५ माघ आइतबार)  
```  

### **Parsing Dates from Strings**  
```python  
npdatetime.datetime.strptime('2077-09-12', '%Y-%m-%d')  
# Output: npdatetime.datetime(2077, 9, 12, 0, 0)  
```  

### **Timedelta Operations**  
```python  
# Adding days to a date  
npdatetime.date(1990, 5, 10) + datetime.timedelta(days=350)  
# Output: npdatetime.date(1991, 4, 26)  

# Adding hours and minutes to a datetime  
npdatetime.datetime(1990, 5, 10, 5, 10) + datetime.timedelta(hours=3, minutes=15)  
# Output: npdatetime.datetime(1990, 5, 10, 8, 25)  
```  

### **Bikram Sambat <-> Gregorian Conversion**  
```python  
# Convert Bikram Sambat to Gregorian  
npdatetime.date(1999, 7, 25).to_datetime_date()  
# Output: datetime.date(1942, 11, 10)  

# Convert Gregorian to Bikram Sambat  
npdatetime.date.from_datetime_date(datetime.date(1942, 11, 10))  
# Output: npdatetime.date(1999, 7, 25)  
```  

### **Bikram Sambat Monthly Calendar**  
```python  
npdatetime.date(2078, 1, 1).calendar()  

# Output:  
          Baishakh 2078  
Sun  Mon  Tue  Wed  Thu  Fri  Sat  
                1    2    3    4  
5     6    7    8    9   10   11  
12   13   14   15   16   17   18  
19   20   21   22   23   24   25  
26   27   28   29   30   31  
```  

---

# Nepali Fiscal Year Module Documentation

This module provides functionality to calculate and manage fiscal year information based on the Nepali calendar. It allows you to customize fiscal year durations, handle leap years, and generate reports about fiscal years, quarters, and fiscal weeks.

## Functions

### `fiscal_year(date_obj=None, start_month=4, end_month=3)`

Returns the fiscal year for the provided Nepali date. If no date is provided, the current date is used. You can also customize the start and end month of the fiscal year.

**Parameters:**
- `date_obj` (optional): A Nepali date object. If not provided, today's date will be used.
- `start_month` (optional): The start month of the fiscal year (default is Shrawan, month 4).
- `end_month` (optional): The end month of the fiscal year (default is Ashad, month 12).

**Returns:**
- A tuple containing the start and end year of the fiscal year.

**Example:**
```python
fiscal_year(date_obj=date(2080, 5, 15), start_month=9, end_month=6)
# Returns: (2080, 2081)
```

---

### `get_fiscal_year(date_obj, start_month=4, end_month=3, format=None)`

Returns the fiscal year based on the Nepali date object, with support for various formats.

**Parameters:**
- `date_obj`: A Nepali date object.
- `start_month` (optional): The start month of the fiscal year (default is Shrawan, month 4).
- `end_month` (optional): The end month of the fiscal year (default is Ashad, month 12).
- `format` (optional): The format for the fiscal year representation. Supported formats:
  - `None` (default): Returns a tuple of `(start_year, end_year)`.
  - `"start_yy/end_yy"`: Returns a string in the format `80/81`.
  - `"start_yyyy-end_yyyy"`: Returns a string in the format `2080-2081`.
  - `"FY start_yyyy/end_yy"`: Returns a string in the format `FY 2080/81`.

**Returns:**
- The fiscal year in the specified format or a tuple of `(start_year, end_year)`.

**Example:**
```python
get_fiscal_year(date_obj=date(2080, 5, 15), format="{start_year}-{end_year}")
# Returns: '2080-2081'
```

---

### `start_of_fiscal_year(year, start_month=4)`

Returns the start date of the fiscal year in Nepali date format.

**Parameters:**
- `year`: The fiscal year for which the start date is required.
- `start_month` (optional): The start month of the fiscal year (default is Shrawan, month 4).

**Returns:**
- A Nepali date object representing the start of the fiscal year.

**Example:**
```python
start_of_fiscal_year(2080, start_month=9)
# Returns: date(2080, 9, 1)
```

---

### `end_of_fiscal_year(year, end_month=3)`

Returns the end date of the fiscal year in Nepali date format.

**Parameters:**
- `year`: The fiscal year for which the end date is required.
- `end_month` (optional): The end month of the fiscal year (default is Ashad, month 12).

**Returns:**
- A Nepali date object representing the end of the fiscal year.

**Example:**
```python
end_of_fiscal_year(2080, end_month=6)
# Returns: date(2081, 6, 30)
```

---

### `get_fiscal_quarter(date_obj, start_month=4)`

Returns the fiscal quarter for the given Nepali date.

**Parameters:**
- `date_obj`: A Nepali date object.
- `start_month` (optional): The start month of the fiscal year (default is Shrawan, month 4).

**Returns:**
- An integer representing the fiscal quarter:
  - 1: Shrawan - Bhadra (months 1–3)
  - 2: Aswin - Magh (months 4–6)
  - 3: Falgun - Jestha (months 7–9)
  - 4: Ashad (months 10–12)

**Example:**
```python
get_fiscal_quarter(date_obj=date(2080, 5, 15))
# Returns: 2 (Aswin - Magh)
```

---

### `fiscal_year_range(start_date, end_date, start_month=4, end_month=3)`

Returns a list of fiscal years for a given date range.

**Parameters:**
- `start_date`: A Nepali date object representing the start of the range.
- `end_date`: A Nepali date object representing the end of the range.
- `start_month` (optional): The start month of the fiscal year (default is Shrawan, month 4).
- `end_month` (optional): The end month of the fiscal year (default is Ashad, month 12).

**Returns:**
- A list of fiscal years for the date range.

**Example:**
```python
fiscal_year_range(start_date=date(2080, 4, 1), end_date=date(2081, 3, 31))
# Returns: [(2080, 2081)]
```

---

### `fiscal_year_report(date_obj, start_month=4, end_month=3)`

Returns a structured JSON report for the fiscal year associated with the given Nepali date. The report includes:
- Fiscal year
- Start and end date
- Fiscal quarter
- Fiscal quarters and their respective date ranges

**Parameters:**
- `date_obj`: A Nepali date object.
- `start_month` (optional): The start month of the fiscal year (default is Shrawan, month 4).
- `end_month` (optional): The end month of the fiscal year (default is Ashad, month 12).

**Returns:**
- A JSON string containing the fiscal year report.

**Example:**
```python
fiscal_year_report(date_obj=date(2080, 5, 15), start_month=9, end_month=6)
# Returns a JSON report with fiscal year, quarters, and their date ranges
```

---

## Private Helper Functions

### `_determine_fiscal_year(date_obj, start_month, end_month)`

Determines the fiscal year for a given Nepali date based on the start and end month.

**Parameters:**
- `date_obj`: A Nepali date object.
- `start_month`: The start month of the fiscal year.
- `end_month`: The end month of the fiscal year.

**Returns:**
- A tuple of `(start_year, end_year)` representing the fiscal year.

### `_format_fiscal_year(start_year, end_year, format)`

Formats the fiscal year into the specified string format.

**Parameters:**
- `start_year`: The start year of the fiscal year.
- `end_year`: The end year of the fiscal year.
- `format`: A string format for fiscal year representation.

**Returns:**
- A string formatted according to the provided `format`.

---

### Example Usage

```python
# Get fiscal year for today's date
print(fiscal_year())

# Get fiscal year for a specific date
print(get_fiscal_year(date(2080, 5, 15)))

# Get fiscal quarter for a specific date
print(get_fiscal_quarter(date(2080, 5, 15)))

# Get fiscal year range for a date range
start_date = date(2080, 4, 1)
end_date = date(2081, 3, 31)
print(fiscal_year_range(start_date, end_date))

# Get fiscal year report for a specific date
print(fiscal_year_report(date(2080, 5, 15)))
```

---

## **Documentation**  

Comprehensive usage examples and detailed documentation can be found on the [official website](https://4mritGiri.github.io/npdatetime/).  

---

## **Contributing**  

We welcome contributions! If you'd like to contribute, check out the [CONTRIBUTING.md](https://github.com/4mritGiri/npdatetime/blob/master/CONTRIBUTING.md) guide for details on how to get started.  

---

## **License**  

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.  

---

## **Feedback & Support**  

For feature requests, bug reports, or feedback, please create an issue on the [GitHub repository](https://github.com/4mritGiri/npdatetime/issues).  

---

### 🌟 **Made for Developers, by Developers** 🌟  
Your feedback and support are invaluable in making **npdatetime** the go-to library for working with Nepali dates. Thank you! 🙌  

---  

### **Improvements in This Version**  
1. Enhanced structure with logical sections for better readability.  
2. Highlighted key functionalities for quick reference.  
3. Added friendly language to engage contributors and users.  
4. Updated examples to be more illustrative and user-friendly.  
