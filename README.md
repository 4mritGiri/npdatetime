# NPDateTime

High-performance Nepali (Bikram Sambat) datetime library for Rust and beyond.

[![Cargo](https://img.shields.io/crates/v/npdatetime.svg)](https://crates.io/crates/npdatetime)
[![Documentation](https://docs.rs/npdatetime/badge.svg)](https://docs.rs/npdatetime)
[![License](https://img.shields.io/crate/l/npdatetime.svg)](LICENSE)

NPDateTime is a modern, fast, and accurate library for working with the Bikram Sambat (BS) calendar. It uniquely combines the speed of lookup tables with the precision of astronomical calculations.

**This version achieves 100% feature parity with the original Python [npdatetime](https://github.com/4mritGiri/npdatetime) library, while adding an advanced high-precision astronomical engine.**

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

NPDateTime achieves exceptional performance through compile-time CSV embedding:

| Operation | Time | Notes |
| :--- | :--- | :--- |
| `days_in_month` | **9-12 ns** | Lookup table access |
| Date creation | **12 ns** | Validates and constructs |
| BS ↔ AD conversion | **6-8 µs** | Full date conversion |
| Format operations | **98-640 ns** | strftime-style formatting |

*Benchmarks on Rust 1.92, release mode*

## 🌍 Multi-Language Support

NPDateTime provides **official bindings** for multiple languages:

### Python (PyO3)
```bash
pip install npdatetime
```

```python
from npdatetime import NepaliDate

date = NepaliDate(2077, 5, 19)
year, month, day = date.to_gregorian()
print(f"{year}-{month:02d}-{day:02d}")  # 2020-09-04
```

### JavaScript/WASM
```bash
npm install npdatetime-wasm
```

```javascript
import init, { NepaliDate } from 'npdatetime-wasm';
await init();

const date = new NepaliDate(2077, 5, 19);
const [year, month, day] = date.toGregorian();
console.log(`${year}-${month}-${day}`);  // 2020-9-4
```

See [`bindings/`](bindings/) for detailed setup and API documentation.

## 📚 Documentation

- **[CHANGELOG](CHANGELOG.md)**: Release notes and version history.
- **[CONTRIBUTING](CONTRIBUTING.md)**: How to contribute.
- **[SECURITY](SECURITY.md)**: Security policy and vulnerability reporting.
- **[Roadmap](docs/ROADMAP.md)**: Future plans and progress.
- **[Development Guide](docs/DEVELOPMENT_GUIDE.md)**: Architecture and coding standards.
- **[Astronomy Theory](docs/ASTRONOMY.md)**: The math behind calculations.
- **[Project Structure](docs/PROJECT_STRUCTURE.md)**: Codebase layout.

## 📂 Project Structure

- `src/core/`: Shared types (`NepaliDate`, error handling, formatting).
- `src/lookup/`: Fast table-based calendar logic (1975-2100 BS).
- `src/astronomical/`: High-precision solar (VSOP87) and lunar (ELP-2000) calculations.
- `bindings/python/`: PyO3 bindings for Python.
- `bindings/javascript/`: wasm-bindgen bindings for JavaScript/WASM.
- `examples/`: Usage examples and demonstrations.
- `benches/`: Performance benchmarks.

## 🧪 Testing

```bash
# Run all tests
cargo test

# Run with all features
cargo test --all-features

# Run benchmarks
cargo bench
```

**Test Coverage:** 67 tests, 100% passing

## 📜 License

This project is licensed under the [MIT License](LICENSE).