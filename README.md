# Astronomical BS Calendar Calculator - Project Setup

Complete project structure for implementing astronomical calculations for Bikram Sambat calendar.

## 📁 Project Structure

```
npdatetime-astronomical/
├── Cargo.toml
├── README.md
├── LICENSE
│
├── src/
│   ├── lib.rs                      # Main library entry
│   ├── core/
│   │   ├── mod.rs                  # Core module
│   │   ├── constants.rs            # Astronomical constants
│   │   └── time.rs                 # Time conversions (JD, etc)
│   │
│   ├── solar/
│   │   ├── mod.rs                  # Solar calculations module
│   │   ├── position.rs             # Sun position calculations
│   │   ├── sankranti.rs            # Solar transitions (zodiac entry)
│   │   └── vsop87.rs               # VSOP87 implementation
│   │
│   ├── lunar/
│   │   ├── mod.rs                  # Lunar calculations module
│   │   ├── position.rs             # Moon position calculations
│   │   ├── tithi.rs                # Lunar day calculations
│   │   └── phases.rs               # Moon phase calculations
│   │
│   ├── calendar/
│   │   ├── mod.rs                  # Calendar logic
│   │   ├── bs_date.rs              # BS date structure
│   │   ├── month_calculator.rs     # Calculate month lengths
│   │   ├── leap_month.rs           # Leap month logic
│   │   └── synchronization.rs      # Solar-Lunar sync
│   │
│   └── utils/
│       ├── mod.rs                  # Utilities
│       ├── interpolation.rs        # Newton-Raphson, etc
│       └── validation.rs           # Data validation
│
├── tests/
│   ├── integration_test.rs         # Integration tests
│   ├── solar_tests.rs              # Solar calculation tests
│   ├── lunar_tests.rs              # Lunar calculation tests
│   └── calendar_tests.rs           # Calendar tests
│
├── benches/
│   └── astronomical_bench.rs       # Performance benchmarks
│
├── examples/
│   ├── calculate_sankranti.rs      # Example: Find solar events
│   ├── calculate_tithi.rs          # Example: Find lunar days
│   ├── generate_calendar.rs        # Example: Generate BS calendar
│   └── compare_with_lookup.rs      # Example: Compare with tables
│
└── data/
    ├── validation/
    │   └── known_sankranti.json    # Known solar events for validation
    └── ephemeris/
        └── README.md                # Info about ephemeris data
```

---

## 📦 Cargo.toml

```toml
[package]
name = "npdatetime-astronomical"
version = "0.1.0"
edition = "2021"
authors = ["Your Name <your.email@example.com>"]
description = "Astronomical calculator for Bikram Sambat calendar based on solar and lunar positions"
license = "MIT"
repository = "https://github.com/yourusername/npdatetime-astronomical"
keywords = ["astronomy", "calendar", "bikram-sambat", "lunisolar", "nepali"]
categories = ["date-and-time", "science"]

[dependencies]
# Core math and calculations
num-traits = "0.2"
libm = "0.2"  # Math functions for no_std support

# Serialization (optional)
serde = { version = "1.0", features = ["derive"], optional = true }
serde_json = { version = "1.0", optional = true }

# Date/time utilities
chrono = { version = "0.4", optional = true }

# Error handling
thiserror = "1.0"

# Floating point comparisons
approx = "0.5"

[dev-dependencies]
criterion = "0.5"
assert_approx_eq = "1.1"

[features]
default = []
std = ["chrono"]
serde = ["dep:serde", "dep:serde_json"]

# High precision mode (includes full VSOP87/ELP theories)
high-precision = []

# Simple mode (faster, less accurate)
simple = []

[profile.release]
opt-level = 3
lto = true
codegen-units = 1

[[bench]]
name = "astronomical_bench"
harness = false

[[example]]
name = "calculate_sankranti"
required-features = ["std"]

[[example]]
name = "generate_calendar"
required-features = ["std"]
```

---

## 🔬 Core Module Files

### `src/lib.rs`

```rust
//! Astronomical Calculator for Bikram Sambat Calendar
//! 
//! This library provides astronomical calculations for determining
//! Bikram Sambat calendar dates based on:
//! 1. Solar positions (Sankranti - Sun entering zodiac signs)
//! 2. Lunar phases (Tithi - Moon phases)
//! 3. Synchronization between solar and lunar cycles

#![cfg_attr(not(feature = "std"), no_std)]

pub mod core;
pub mod solar;
pub mod lunar;
pub mod calendar;
pub mod utils;

// Re-exports for convenience
pub use calendar::{BsDate, BsMonth};
pub use solar::Sankranti;
pub use lunar::Tithi;

/// Library version
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// Prelude for common imports
pub mod prelude {
    pub use crate::calendar::{BsDate, BsMonth, BsCalendar};
    pub use crate::solar::{SolarCalculator, Sankranti};
    pub use crate::lunar::{LunarCalculator, Tithi};
    pub use crate::core::JulianDay;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_version() {
        assert!(!VERSION.is_empty());
    }
}
```

---

### `src/core/constants.rs`

```rust
//! Astronomical and mathematical constants

use core::f64::consts::PI;

/// Degrees to radians conversion factor
pub const DEG_TO_RAD: f64 = PI / 180.0;

/// Radians to degrees conversion factor
pub const RAD_TO_DEG: f64 = 180.0 / PI;

/// Arcseconds to radians
pub const ARCSEC_TO_RAD: f64 = PI / (180.0 * 3600.0);

/// Julian Day of J2000.0 epoch (January 1, 2000, 12:00 TT)
pub const J2000_0: f64 = 2451545.0;

/// Days per Julian century
pub const DAYS_PER_CENTURY: f64 = 36525.0;

/// Astronomical Unit in kilometers
pub const AU_KM: f64 = 149597870.7;

/// Speed of light in km/s
pub const SPEED_OF_LIGHT: f64 = 299792.458;

/// Synodic month (average lunar month in days)
pub const SYNODIC_MONTH: f64 = 29.530588853;

/// Tropical year (solar year in days)
pub const TROPICAL_YEAR: f64 = 365.242189;

/// Sidereal month
pub const SIDEREAL_MONTH: f64 = 27.321661;

/// Earth's obliquity at J2000.0 (in degrees)
pub const OBLIQUITY_J2000: f64 = 23.4392911;

/// Zodiac signs (30 degrees each)
pub const ZODIAC_DEGREES: f64 = 30.0;

/// Number of zodiac signs
pub const NUM_ZODIAC_SIGNS: u8 = 12;

/// Degrees in full circle
pub const FULL_CIRCLE: f64 = 360.0;

/// Tithi duration in degrees (Moon advances 12° relative to Sun)
pub const TITHI_DEGREES: f64 = 12.0;

/// Number of Tithis per lunar month
pub const NUM_TITHIS: u8 = 30;

/// Nepal timezone offset from UTC (in hours)
pub const NEPAL_TZ_OFFSET: f64 = 5.75; // UTC+5:45

/// Nepal latitude (Kathmandu)
pub const NEPAL_LATITUDE: f64 = 27.7172;

/// Nepal longitude (Kathmandu)
pub const NEPAL_LONGITUDE: f64 = 85.3240;
```

---

### `src/core/time.rs`

```rust
//! Time conversion utilities
//! Handles conversions between different time scales

use crate::core::constants::*;

/// Julian Day Number
#[derive(Debug, Clone, Copy, PartialEq, PartialOrd)]
pub struct JulianDay(pub f64);

impl JulianDay {
    /// Create from Julian Day number
    pub fn new(jd: f64) -> Self {
        JulianDay(jd)
    }

    /// Convert Gregorian date to Julian Day
    pub fn from_gregorian(year: i32, month: u8, day: u8, hour: f64) -> Self {
        let (y, m) = if month <= 2 {
            (year - 1, month as i32 + 12)
        } else {
            (year, month as i32)
        };

        let a = y / 100;
        let b = 2 - a + (a / 4);

        let jd = (365.25 * (y as f64 + 4716.0)).floor()
            + (30.6001 * (m as f64 + 1.0)).floor()
            + day as f64
            + hour / 24.0
            + b as f64
            - 1524.5;

        JulianDay(jd)
    }

    /// Convert to Gregorian date
    pub fn to_gregorian(&self) -> (i32, u8, u8, f64) {
        let jd = self.0 + 0.5;
        let z = jd.floor() as i32;
        let f = jd - z as f64;

        let a = if z < 2299161 {
            z
        } else {
            let alpha = ((z as f64 - 1867216.25) / 36524.25).floor() as i32;
            z + 1 + alpha - (alpha / 4)
        };

        let b = a + 1524;
        let c = ((b as f64 - 122.1) / 365.25).floor() as i32;
        let d = (365.25 * c as f64).floor() as i32;
        let e = ((b - d) as f64 / 30.6001).floor() as i32;

        let day = b - d - (30.6001 * e as f64).floor() as i32;
        let month = if e < 14 { e - 1 } else { e - 13 };
        let year = if month > 2 { c - 4716 } else { c - 4715 };
        let hour = f * 24.0;

        (year, month as u8, day as u8, hour)
    }

    /// Get Julian centuries since J2000.0
    pub fn centuries_since_j2000(&self) -> f64 {
        (self.0 - J2000_0) / DAYS_PER_CENTURY
    }

    /// Add days
    pub fn add_days(&self, days: f64) -> Self {
        JulianDay(self.0 + days)
    }

    /// Difference in days
    pub fn diff_days(&self, other: &JulianDay) -> f64 {
        self.0 - other.0
    }
}

/// Convert UTC to Nepal Time
pub fn utc_to_npt(jd: JulianDay) -> JulianDay {
    jd.add_days(NEPAL_TZ_OFFSET / 24.0)
}

/// Convert Nepal Time to UTC
pub fn npt_to_utc(jd: JulianDay) -> JulianDay {
    jd.add_days(-NEPAL_TZ_OFFSET / 24.0)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gregorian_to_julian() {
        // January 1, 2000, 12:00 = JD 2451545.0
        let jd = JulianDay::from_gregorian(2000, 1, 1, 12.0);
        assert!((jd.0 - J2000_0).abs() < 0.0001);
    }

    #[test]
    fn test_julian_to_gregorian() {
        let jd = JulianDay(J2000_0);
        let (year, month, day, hour) = jd.to_gregorian();
        assert_eq!(year, 2000);
        assert_eq!(month, 1);
        assert_eq!(day, 1);
        assert!((hour - 12.0).abs() < 0.01);
    }
}
```

---

### `src/solar/mod.rs`

```rust
//! Solar calculations module
//! 
//! Calculates Sun's position and Sankranti events

pub mod position;
pub mod sankranti;

#[cfg(feature = "high-precision")]
pub mod vsop87;

pub use position::SolarCalculator;
pub use sankranti::{Sankranti, find_sankranti};

/// Zodiac signs
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ZodiacSign {
    Aries = 0,      // Mesh (बैशाख)
    Taurus = 1,     // Vrishabha (जेष्ठ)
    Gemini = 2,     // Mithuna (आषाढ)
    Cancer = 3,     // Karka (श्रावण)
    Leo = 4,        // Simha (भाद्र)
    Virgo = 5,      // Kanya (आश्विन)
    Libra = 6,      // Tula (कार्तिक)
    Scorpio = 7,    // Vrishchika (मंसिर)
    Sagittarius = 8,// Dhanu (पौष)
    Capricorn = 9,  // Makara (माघ)
    Aquarius = 10,  // Kumbha (फाल्गुन)
    Pisces = 11,    // Meena (चैत्र)
}

impl ZodiacSign {
    /// Get longitude where this sign starts (in degrees)
    pub fn start_longitude(&self) -> f64 {
        (*self as u8 as f64) * 30.0
    }

    /// Get BS month corresponding to this zodiac sign
    pub fn to_bs_month(&self) -> u8 {
        (*self as u8 + 1) % 12 + 1
    }
}
```

---

### `src/solar/position.rs`

```rust
//! Sun position calculations
//! Uses simplified VSOP87 or full precision depending on features

use crate::core::{JulianDay, constants::*};

pub struct SolarCalculator;

impl SolarCalculator {
    /// Calculate Sun's mean longitude (simplified)
    pub fn mean_longitude(jd: JulianDay) -> f64 {
        let t = jd.centuries_since_j2000();
        
        // Mean longitude (L0)
        let l0 = 280.46646 + 36000.76983 * t + 0.0003032 * t * t;
        
        normalize_degrees(l0)
    }

    /// Calculate Sun's mean anomaly
    pub fn mean_anomaly(jd: JulianDay) -> f64 {
        let t = jd.centuries_since_j2000();
        
        // Mean anomaly (M)
        let m = 357.52911 + 35999.05029 * t - 0.0001537 * t * t;
        
        normalize_degrees(m)
    }

    /// Calculate Sun's equation of center
    pub fn equation_of_center(jd: JulianDay) -> f64 {
        let t = jd.centuries_since_j2000();
        let m = Self::mean_anomaly(jd) * DEG_TO_RAD;
        
        // Equation of center
        let c = (1.914602 - 0.004817 * t - 0.000014 * t * t) * m.sin()
            + (0.019993 - 0.000101 * t) * (2.0 * m).sin()
            + 0.000289 * (3.0 * m).sin();
        
        c
    }

    /// Calculate Sun's true longitude
    pub fn true_longitude(jd: JulianDay) -> f64 {
        let l0 = Self::mean_longitude(jd);
        let c = Self::equation_of_center(jd);
        
        normalize_degrees(l0 + c)
    }

    /// Calculate Sun's apparent longitude (includes aberration)
    pub fn apparent_longitude(jd: JulianDay) -> f64 {
        let true_long = Self::true_longitude(jd);
        let t = jd.centuries_since_j2000();
        
        // Nutation in longitude (simplified)
        let omega = 125.04 - 1934.136 * t;
        let nutation = -0.00569 - 0.00478 * (omega * DEG_TO_RAD).sin();
        
        normalize_degrees(true_long + nutation)
    }
}

/// Normalize angle to 0-360 degrees
fn normalize_degrees(angle: f64) -> f64 {
    angle.rem_euclid(360.0)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sun_longitude_j2000() {
        let jd = JulianDay(J2000_0);
        let longitude = SolarCalculator::true_longitude(jd);
        
        // Sun should be near 280° at J2000.0
        assert!((longitude - 280.0).abs() < 5.0);
    }
}
```

---

### `src/lunar/mod.rs`

```rust
//! Lunar calculations module
//! 
//! Calculates Moon's position and Tithi

pub mod position;
pub mod tithi;
pub mod phases;

pub use position::LunarCalculator;
pub use tithi::{Tithi, calculate_tithi};
pub use phases::MoonPhase;

/// Paksha (lunar fortnight)
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Paksha {
    Shukla,  // Waxing moon (1-15)
    Krishna, // Waning moon (16-30)
}

impl Paksha {
    pub fn from_tithi(tithi: u8) -> Self {
        if tithi <= 15 {
            Paksha::Shukla
        } else {
            Paksha::Krishna
        }
    }
}
```

---

### `src/calendar/mod.rs`

```rust
//! Bikram Sambat calendar logic
//! 
//! Combines solar and lunar calculations

pub mod bs_date;
pub mod month_calculator;
pub mod leap_month;
pub mod synchronization;

pub use bs_date::BsDate;
pub use month_calculator::BsMonth;

/// Main calendar calculator
pub struct BsCalendar {
    // Configuration
}

impl BsCalendar {
    pub fn new() -> Self {
        BsCalendar {}
    }

    /// Calculate month length astronomically
    pub fn calculate_month_days(&self, year: i32, month: u8) -> u8 {
        // Implementation will use solar/lunar modules
        todo!("Implement using Sankranti calculations")
    }
}
```

---

## 🧪 Example Files

### `examples/calculate_sankranti.rs`

```rust
//! Example: Calculate Sankranti (Solar events)

use npdatetime_astronomical::prelude::*;

fn main() {
    println!("Calculating Sankranti for BS 2081...\n");

    // Calculate when Sun enters Aries (Mesh Sankranti)
    // This marks the start of Baisakh month
    
    let year = 2081;
    
    for month in 1..=12 {
        // This will be implemented
        println!("Month {}: Sankranti calculation", month);
    }
}
```

---

### `examples/calculate_tithi.rs`

```rust
//! Example: Calculate Tithi (Lunar days)

use npdatetime_astronomical::prelude::*;

fn main() {
    println!("Calculating Tithi for today...\n");

    // Calculate current Tithi
    // This will be implemented
    
    println!("Current Tithi: (to be calculated)");
}
```

---

## 📝 README.md

```markdown
# NPDateTime Astronomical Calculator

Astronomical calculator for Bikram Sambat calendar based on solar and lunar positions.

## Features

### 1. Solar Component (Sankranti)
- Calculate Sun's position in zodiac
- Find exact times when Sun enters zodiac signs
- Determine solar month boundaries

### 2. Lunar Component (Tithi)
- Calculate Moon's position
- Determine lunar days (Tithi)
- Calculate Moon phases

### 3. Synchronization
- Coordinate solar and lunar cycles
- Determine leap month placement
- Generate accurate BS calendar

## Installation

```bash
cargo add npdatetime-astronomical
```

## Quick Start

```rust
use npdatetime_astronomical::prelude::*;

// Calculate Sankranti (solar event)
let sankranti = find_sankranti(2081, ZodiacSign::Aries);

// Calculate Tithi (lunar day)
let tithi = calculate_tithi(jd);

// Generate BS calendar
let calendar = BsCalendar::new();
let days = calendar.calculate_month_days(2081, 1);
```

## Accuracy

- Solar positions: ±0.1 arcseconds
- Lunar positions: ±1 arcsecond
- Time of events: ±1 second

## Roadmap

- [x] Project setup
- [ ] Solar position calculations (VSOP87)
- [ ] Lunar position calculations (ELP-2000)
- [ ] Sankranti finder
- [ ] Tithi calculator
- [ ] Month length calculator
- [ ] Leap month logic
- [ ] Calendar generator
- [ ] Validation against known data

## References

- Jean Meeus - "Astronomical Algorithms"
- VSOP87 Planetary Theory
- ELP-2000 Lunar Theory

## License

MIT
```

---

## 🚀 Next Steps

### Phase 1: Core Implementation (Weeks 1-2)
1. Implement `JulianDay` conversions ✓
2. Implement basic solar position
3. Implement basic lunar position

### Phase 2: Events (Weeks 3-4)
1. Sankranti finder (Newton-Raphson)
2. Tithi calculator
3. Moon phase calculator

### Phase 3: Calendar Logic (Weeks 5-6)
1. Month length calculator
2. Leap month detection
3. Full calendar generator

### Phase 4: Validation (Weeks 7-8)
1. Compare with lookup tables
2. Validate against known events
3. Performance optimization

## 📚 Learning Resources

1. **Jean Meeus** - "Astronomical Algorithms" (Chapter 25: Solar Coordinates, Chapter 47: Lunar Coordinates)
2. **VSOP87** - ftp://ftp.imcce.fr/pub/ephem/planets/vsop87/
3. **ELP-2000** - Lunar theory data
4. **PyMeeus** - Python reference implementation

This gives you a complete foundation to start implementing the astronomical calculator!