# NPDateTime User Guide 🇳🇵

NPDateTime is a modern, fast, and accurate library for working with the Bikram Sambat (BS) calendar.

## 🚀 Quick Start

### Installation

Add this to your `Cargo.toml`:
```toml
[dependencies]
npdatetime = "0.1.0"
```

### Basic Usage

```rust
use npdatetime::prelude::*;

fn main() -> Result<()> {
    // Create a date
    let date = NepaliDate::new(2077, 5, 19)?;
    println!("Standard BS: {}", date); // 2077-05-19

    // Convert to Gregorian (AD)
    let (year, month, day) = date.to_gregorian()?;
    println!("AD Date: {}-{:02}-{:02}", year, month, day); // 2020-09-04

    // Parse from string
    let parsed = NepaliDate::parse("2077-05-19", "%Y-%m-%d")?;
    assert_eq!(date, parsed);

    Ok(())
}
```

## 📅 Calendar Logic

NPDateTime uses a **hybrid approach**:
1. **Lookup Tables**: For years 1975 to 2100 BS, it uses pre-validated calendar data for 100% accuracy and maximum speed (~10ns).
2. **Astronomical Engine**: For future or historical dates outside the lookup range, it can calculate month lengths using VSOP87 (solar) and ELP-2000 (lunar) models.

### Using the Astronomical Engine
Enable the `astronomical` feature:
```toml
npdatetime = { version = "0.1.0", features = ["astronomical"] }
```

```rust
use npdatetime::astronomical::BsCalendar;

let cal = BsCalendar::new();
let info = cal.get_year_info(2081)?;
println!("Year 2081 month lengths: {:?}", info.month_lengths);
```

## 🛠 Features

### Date Arithmetic
```rust
let today = NepaliDate::today()?;
let next_month = today.add_days(30)?;
let previous_week = today.add_days(-7)?;
```

### Fiscal Year and Ordinals (Feature Parity)
NPDateTime now includes full parity with the original Python `npdatetime` library:

```rust
let date = NepaliDate::new(2080, 4, 15)?;
println!("Fiscal Year: {}", date.fiscal_year());    // "2080/81"
println!("Quarter: {}", date.fiscal_quarter());     // 1

let ordinal = date.to_ordinal();
let back = NepaliDate::from_ordinal(ordinal)?;
assert_eq!(date, back);
```

### Formatting (Extensive Tokens)
| Token | Description | Example |
|-------|-------------|---------|
| `%K`  | Devanagari Year | २०७७ |
| `%n`  | Devanagari Month | ०५ |
| `%D`  | Devanagari Day | १९ |
| `%N`  | Devanagari Month Name | भाद्र |
| `%G`  | Devanagari Weekday | शुक्रवार |

### Visual Calendar
```rust
let date = NepaliDate::today()?;
println!("{}", date.month_calendar());
```

### Tithis and Sankrantis
Requires `astronomical` feature:
```rust
use npdatetime::astronomical::{SankrantiFinder, TithiCalculator};
use npdatetime::astronomical::core::JulianDay;

let jd = JulianDay::from_gregorian(2024, 4, 13, 12.0);
let tithi = TithiCalculator::get_tithi(jd);
println!("Tithi: {} ({})", tithi.name(), tithi.paksha);
```

## 🌍 Language Bindings

NPDateTime is designed to be used everywhere:
- **Python**: `pip install npdatetime`
- **JavaScript/WASM**: `npm install @4mritgiri/npdatetime`
- **Java/Stubs**: Available in `bindings/java`

## 📊 Performance Tips

- Use the **default lookup tables** for high-volume transactions.
- Use **formatting patterns** once or cache formatted strings if needed, though formatting is very fast (<1µs).
- Avoid unnecessary round-trips to Gregorian if only BS operations are needed.

## ❓ FAQ

### Why use NPDateTime over other libraries?
Most existing libraries for Nepali dates are either inaccurate (using approximations) or slow (reading files at runtime). NPDateTime is verified and embeds data at compile time.

### Is it `no_std` compatible?
The core library is `no_std` compatible if you disable the `std` feature.

### Can I contribute?
Yes! See [CONTRIBUTING.md](../CONTRIBUTING.md).
