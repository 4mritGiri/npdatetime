# NPDateTime

High-performance Nepali (Bikram Sambat) datetime library for Rust and beyond.

[![Cargo](https://img.shields.io/crates/v/npdatetime.svg)](https://crates.io/crates/npdatetime)
[![Documentation](https://docs.rs/npdatetime/badge.svg)](https://docs.rs/npdatetime)
[![License](https://img.shields.io/crate/l/npdatetime.svg)](LICENSE)

NPDateTime is a modern, fast, and accurate library for working with the Bikram Sambat (BS) calendar. It uniquely combines the speed of lookup tables with the precision of astronomical calculations.

## 🌟 Key Design Decisions

- **Hybrid Engine**: Use `lookup-tables` for historical accuracy (1975-2100 BS) or `astronomical` for high-precision calculations based on VSOP87 and ELP-2000 theories.
- **Zero Overhead**: Minimal dependencies and `no_std` compatibility for embedded systems.
- **Feature Flags**: Take only what you need. Small binary size by default.
- **Reliability**: Verified against official government calendars and astronomical ephemeris.

## 🚀 Quick Start

Add to your `Cargo.toml`:

```toml
[dependencies]
npdatetime = "0.1.0"
```

### Basic Usage

```rust
use npdatetime::prelude::*;

fn main() -> Result<()> {
    // Create a Nepali Date
    let date = NepaliDate::new(2081, 1, 1)?;
    println!("Standard BS: {}", date);

    // Convert to Gregorian
    let (year, month, day) = date.to_gregorian()?;
    println!("AD Date: {}-{:02}-{:02}", year, month, day);

    Ok(())
}
```

### Astronomical Calculations

Enable the `astronomical` feature to access high-precision tools:

```rust
#[cfg(feature = "astronomical")]
{
    let cal = AstronomicalCalendar::new();
    let info = cal.get_year_info(2081)?;
    println!("Months: {:?}", info.month_lengths);
}
```

## 🛠 Feature Flags

| Feature | Description | Default |
| :--- | :--- | :--- |
| `lookup-tables` | Embedded CSV data (1975-2100 BS) | Yes |
| `astronomical` | High-precision solar/lunar models | No |
| `std` | Standard library features (Chrono) | No |
| `wasm` | JS/WASM interop support | No |
| `python` | PyO3 bindings | No |

## 📊 Performance

NPDateTime is designed for high-throughput applications.

| Operation | Lookup Method | Astronomical |
| :--- | :--- | :--- |
| `days_in_month` | ~8 ns | ~690 µs |
| `to_gregorian` | ~8.5 µs | N/A |

*(Benchmarks performed on local environment)*

## 📚 Documentation

- **[Contributing](CONTRIBUTING.md)**: How to get involved.
- **[Roadmap](docs/ROADMAP.md)**: Future plans and progress.
- **[Development Guide](docs/DEVELOPMENT_GUIDE.md)**: Architecture and coding standards.
- **[Astronomy Theory](docs/ASTRONOMY.md)**: The math behind the calculations.

## 📂 Project Structure

- `src/core/`: Shared types (`NepaliDate`, `NpdatetimeError`).
- `src/lookup/`: Table-based civil calendar logic.
- `src/astronomical/`: Solar (VSOP87) and Lunar (ELP-2000) models.
- `bindings/`: Support for Python, JS, Java, and PHP.

## 📜 License

This project is licensed under the [MIT License](LICENSE).