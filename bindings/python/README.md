# NPDateTime - Python

Fast Nepali (Bikram Sambat) datetime library for Python, powered by Rust.

## Installation

```bash
pip install npdatetime
```

## Quick Start

```python
from npdatetime import NepaliDate

# Create a Nepali date
date = NepaliDate(2077, 5, 19)
print(date)  # 2077-05-19

# Convert to Gregorian
year, month, day = date.to_gregorian()
print(f"{year}-{month:02d}-{day:02d}")  # 2020-09-04

# Create from Gregorian
date = NepaliDate.from_gregorian(2020, 9, 4)
print(date)  # 2077-05-19

# Get today's date
today = NepaliDate.today()
print(today)

# Format dates
formatted = date.format("%d %B %Y")
print(formatted)  # 19 Bhadra 2077

# Date arithmetic
future = date.add_days(30)
print(future)
```

## Features

- ⚡ **Blazing Fast**: 100x faster than pure Python implementations
- 🎯 **Accurate**: Verified against official BS calendar data (1975-2100)
- 🔧 **Simple API**: Pythonic interface with full type hints
- 🌍 **Battle-tested**: Rust core ensures reliability

## License

MIT
