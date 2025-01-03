# **Nepali Datetime (Bikram Sambat Date & Nepal Time)**

A Python library inspired by the core `datetime` module, designed for operations based on the **Bikram Sambat (B.S.)** calendar and **Nepal Time (NPT)** timezone (`UTC+05:45`).

### **Key Features**
- Supports Bikram Sambat (B.S.) date operations.
- Handles Nepal Time (NPT) timezone.
- Compatible with Python 3.5+.
- Seamless integration with Python's native `datetime` functionalities.
- Support for date formatting with Nepali Unicode.

---

## **Installation**

Install the package using `pip`:

```bash
pip install npdatetime
```

---

## **Basic Usage**

Here's how you can use `npdatetime` alongside Python's `datetime`:

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

### **Date/Datetime Formatting**
```python
# Formatting Bikram Sambat date
npdatetime.datetime(2077, 5, 19, 8, 26, 10, 123456).strftime("%d %B %Y")
# Output: 19 Bhadau 2077

# Formatting with Nepali Unicode
npdatetime.date(1977, 10, 25).strftime('%K-%n-%D (%k %N %G)')
# Output: १९७७-१०-२५ (७७ माघ आइतबार)
```

### **Parsing from String**
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
npdatetime.datetime(1990, 5, 10, 5, 10, 20) + datetime.timedelta(hours=3, minutes=15)
# Output: npdatetime.datetime(1990, 5, 10, 8, 25, 20)
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

## **Documentation**

Comprehensive usage and examples can be found in the [official documentation](https://4mritGiri.github.io/npdatetime/).

---

## **Contribution**

Contributions are highly encouraged!  
Refer to the [CONTRIBUTING.md](https://github.com/4mritGiri/npdatetime/blob/master/CONTRIBUTING.md) guide for details on how to get started.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

## **Feedback & Support**

For feature requests, bugs, or feedback, please raise an issue on [GitHub](https://github.com/4mritGiri/npdatetime/issues).