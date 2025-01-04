# **Nepali Datetime (Bikram Sambat Date & Nepal Time)**  

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

## **Fiscal Year Calculations**

The **npdatetime** library provides methods to easily calculate the current fiscal year and convert dates to their corresponding fiscal year. Fiscal years in Nepal start from **Shrawan (month 4)** and end at **Ashadh (month 12)**.

### **Getting the Current Fiscal Year**
You can get the current fiscal year using the `current_fiscal_year()` method. It returns the fiscal year as a tuple in the format `(start_year, end_year)`.

```python
import npdatetime

# Get current fiscal year
npdatetime.datetime.current_fiscal_year()
# Output: (2081, 2082)
```

Alternatively, you can use it directly from the `datetime` class:

```python
from npdatetime import datetime

# Get current fiscal year
datetime.current_fiscal_year()
# Output: (2081, 2082)
```

### **Getting Fiscal Year for a Specific Date**
You can also calculate the fiscal year for any specific Nepali date using the `get_fiscal_year_by_date()` function. This takes a `datetime` object as input and returns the fiscal year for that date.

```python
from npdatetime import get_fiscal_year_by_date
from npdatetime import datetime

# Example date
date_obj = datetime(2079, 12, 1)

# Get fiscal year for a specific date
get_fiscal_year_by_date(date_obj)
# Output: (2079, 2080)

# You can also directly pass a Nepali datetime object to the function
get_fiscal_year_by_date(datetime(2080, 4, 1))
# Output: (2080, 2081)
```

### **Examples**

Here are a few examples of how you can use the `get_fiscal_year_by_date()` method to calculate the fiscal year for various dates:

```python
# For 2079-12-01
get_fiscal_year_by_date(datetime(2079, 12, 1))
# Output: (2079, 2080)

# For 2080-03-01
get_fiscal_year_by_date(datetime(2080, 3, 1))
# Output: (2079, 2080)

# For 2080-04-01
get_fiscal_year_by_date(datetime(2080, 4, 1))
# Output: (2080, 2081)

# For 2080-06-01
get_fiscal_year_by_date(datetime(2080, 6, 1))
# Output: (2080, 2081)
```

### **Note**
- The fiscal year is based on the Nepali date system, which is different from the Gregorian calendar. In Nepal, the fiscal year runs from **Shrawan (month 4)** to **Ashadh (month 12)**.

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
