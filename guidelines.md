# Complete Implementation Guidelines
## NPDateTime Astronomical Calculator for Bikram Sambat

**Version:** 1.0  
**Last Updated:** January 2026  
**Purpose:** Astronomical calculation of Bikram Sambat calendar dates based on solar and lunar positions

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture Principles](#architecture-principles)
3. [Module Implementation Order](#module-implementation-order)
4. [Code Standards](#code-standards)
5. [Mathematical Foundations](#mathematical-foundations)
6. [Implementation Details](#implementation-details)
7. [Testing Strategy](#testing-strategy)
8. [Performance Requirements](#performance-requirements)
9. [Validation Process](#validation-process)
10. [Common Pitfalls](#common-pitfalls)

---

## 1. Project Overview

### 1.1 Goals

**Primary Goal:** Calculate Bikram Sambat calendar dates using astronomical positions of Sun and Moon

**Secondary Goals:**
- Validate existing lookup table data
- Generate future calendar data (beyond 2090 BS)
- Provide educational tool for understanding BS calendar mechanics
- Research tool for calendar scientists

### 1.2 Non-Goals

- ❌ Replace lookup tables for production use (too slow)
- ❌ Provide real-time astronomical observations
- ❌ Calculate for dates before 2000 BS (insufficient historical data)
- ❌ Support other calendar systems

### 1.3 Success Criteria

- ✅ Match known Sankranti times within ±10 seconds
- ✅ Match lookup table month lengths 100% for 2000-2090 BS
- ✅ Calculate month length in < 50ms
- ✅ Work without network/external dependencies

---

## 2. Architecture Principles

### 2.1 Separation of Concerns

**RULE 1:** Keep astronomical calculations separate from calendar logic

```rust
// CORRECT: Separation
let sun_longitude = solar::position::calculate(jd);
let month_start = calendar::find_month_start(sun_longitude);

// WRONG: Mixed concerns
let month_start = calculate_month_start_with_sun_position(jd);
```

**RULE 2:** Time conversions in one place only (`core::time`)

```rust
// CORRECT: Centralized
use crate::core::time::JulianDay;
let jd = JulianDay::from_gregorian(2020, 4, 14, 0.0);

// WRONG: Scattered conversions
let jd = year * 365.25 + month * 30.0; // Don't do this!
```

**RULE 3:** Constants defined once in `core::constants`

```rust
// CORRECT: Use constants
use crate::core::constants::ZODIAC_DEGREES;
let sign_boundary = sign_number as f64 * ZODIAC_DEGREES;

// WRONG: Magic numbers
let sign_boundary = sign_number as f64 * 30.0; // What is 30?
```

### 2.2 Modularity

Each module must be **independently testable**:

```rust
// Solar module works alone
#[test]
fn test_solar_position() {
    let jd = JulianDay::from_gregorian(2020, 4, 14, 0.0);
    let longitude = SolarCalculator::true_longitude(jd);
    assert!(longitude >= 0.0 && longitude < 360.0);
}

// Lunar module works alone
#[test]
fn test_lunar_position() {
    let jd = JulianDay::from_gregorian(2020, 4, 14, 0.0);
    let longitude = LunarCalculator::true_longitude(jd);
    assert!(longitude >= 0.0 && longitude < 360.0);
}

// Calendar module uses both
#[test]
fn test_tithi() {
    let jd = JulianDay::from_gregorian(2020, 4, 14, 0.0);
    let tithi = calculate_tithi(jd);
    assert!(tithi >= 1 && tithi <= 30);
}
```

### 2.3 Feature Flags

**RULE 4:** Support multiple accuracy levels

```toml
[features]
default = ["simple"]
simple = []           # Fast, ±10 second accuracy
high-precision = []   # Slow, ±1 second accuracy
validation = ["serde"] # For comparing with lookup tables
```

```rust
// Implementation
#[cfg(feature = "simple")]
pub fn sun_longitude(jd: JulianDay) -> f64 {
    // Simplified 10-term series
}

#[cfg(feature = "high-precision")]
pub fn sun_longitude(jd: JulianDay) -> f64 {
    // Full VSOP87 with 100+ terms
}
```

---

## 3. Module Implementation Order

### Phase 1: Foundation (Week 1)

**Priority: CRITICAL - DO THIS FIRST**

#### 3.1.1 Implement `src/core/time.rs`

**Status:** ✅ Already provided in project setup

**Validation Tests:**

```rust
#[test]
fn test_j2000_epoch() {
    let jd = JulianDay::from_gregorian(2000, 1, 1, 12.0);
    assert_eq!(jd.0, 2451545.0);
}

#[test]
fn test_bs_epoch() {
    // 2000 Baisakh 1 = 1943 April 14
    let jd = JulianDay::from_gregorian(1943, 4, 14, 0.0);
    let (y, m, d, _) = jd.to_gregorian();
    assert_eq!((y, m, d), (1943, 4, 14));
}

#[test]
fn test_round_trip() {
    let jd1 = JulianDay::from_gregorian(2020, 4, 14, 6.5);
    let (y, m, d, h) = jd1.to_gregorian();
    let jd2 = JulianDay::from_gregorian(y, m, d, h);
    assert!((jd1.0 - jd2.0).abs() < 0.0001);
}
```

#### 3.1.2 Implement `src/core/constants.rs`

**Status:** ✅ Already provided

**Validation:** Ensure all constants match astronomical standards

```rust
#[test]
fn test_constants() {
    // Synodic month should be ~29.53 days
    assert!((SYNODIC_MONTH - 29.53).abs() < 0.01);
    
    // Tropical year should be ~365.24 days
    assert!((TROPICAL_YEAR - 365.24).abs() < 0.01);
    
    // Full circle
    assert_eq!(FULL_CIRCLE, 360.0);
}
```

### Phase 2: Solar Calculations (Week 2)

**Priority: HIGH**

#### 3.2.1 Implement `src/solar/position.rs`

**Mathematical Foundation:** Jean Meeus Chapter 25

**Required Functions:**

```rust
impl SolarCalculator {
    /// Mean longitude of Sun
    /// Accuracy: ±0.01 degrees
    /// Reference: Meeus eq. 25.2
    pub fn mean_longitude(jd: JulianDay) -> f64 {
        let t = jd.centuries_since_j2000();
        
        // L0 = 280.46646° + 36000.76983°T + 0.0003032°T²
        let l0 = 280.46646 + 36000.76983 * t + 0.0003032 * t * t;
        
        normalize_degrees(l0)
    }
    
    /// Mean anomaly of Sun
    /// Accuracy: ±0.01 degrees
    /// Reference: Meeus eq. 25.3
    pub fn mean_anomaly(jd: JulianDay) -> f64 {
        let t = jd.centuries_since_j2000();
        
        // M = 357.52911° + 35999.05029°T - 0.0001537°T²
        let m = 357.52911 + 35999.05029 * t - 0.0001537 * t * t;
        
        normalize_degrees(m)
    }
    
    /// Equation of center (Sun)
    /// Accuracy: ±0.001 degrees
    /// Reference: Meeus eq. 25.4
    pub fn equation_of_center(jd: JulianDay) -> f64 {
        let t = jd.centuries_since_j2000();
        let m = Self::mean_anomaly(jd) * DEG_TO_RAD;
        
        // C = (1.914602° - 0.004817°T - 0.000014°T²) sin M
        //   + (0.019993° - 0.000101°T) sin 2M
        //   + 0.000289° sin 3M
        
        let c = (1.914602 - 0.004817 * t - 0.000014 * t * t) * m.sin()
            + (0.019993 - 0.000101 * t) * (2.0 * m).sin()
            + 0.000289 * (3.0 * m).sin();
        
        c
    }
    
    /// True longitude of Sun
    /// Accuracy: ±0.01 degrees
    pub fn true_longitude(jd: JulianDay) -> f64 {
        let l0 = Self::mean_longitude(jd);
        let c = Self::equation_of_center(jd);
        normalize_degrees(l0 + c)
    }
    
    /// Apparent longitude (with nutation and aberration)
    /// Accuracy: ±0.001 degrees
    /// Reference: Meeus eq. 25.8, 25.9
    pub fn apparent_longitude(jd: JulianDay) -> f64 {
        let true_long = Self::true_longitude(jd);
        let t = jd.centuries_since_j2000();
        
        // Nutation in longitude (simplified)
        // Ω = 125.04° - 1934.136°T
        let omega = 125.04 - 1934.136 * t;
        let nutation = -0.00569 - 0.00478 * (omega * DEG_TO_RAD).sin();
        
        // Aberration = -0.00569°
        let aberration = -0.00569;
        
        normalize_degrees(true_long + nutation + aberration)
    }
}
```

**Validation Tests:**

```rust
#[test]
fn test_sun_j2000() {
    // At J2000.0, Sun's mean longitude should be ~280.46°
    let jd = JulianDay(J2000_0);
    let l0 = SolarCalculator::mean_longitude(jd);
    assert!((l0 - 280.46).abs() < 0.1);
}

#[test]
fn test_sun_2020_april() {
    // April 14, 2020 - Sun should be in Aries (~24° in zodiac)
    let jd = JulianDay::from_gregorian(2020, 4, 14, 12.0);
    let longitude = SolarCalculator::apparent_longitude(jd);
    
    // Sun in Aries: 0° - 30°
    assert!(longitude >= 0.0 && longitude < 30.0);
}

#[test]
fn test_sun_monotonic() {
    // Sun's longitude should increase monotonically
    let jd1 = JulianDay::from_gregorian(2020, 1, 1, 0.0);
    let jd2 = jd1.add_days(1.0);
    
    let long1 = SolarCalculator::apparent_longitude(jd1);
    let long2 = SolarCalculator::apparent_longitude(jd2);
    
    // Sun moves ~1° per day
    let diff = (long2 - long1 + 360.0).rem_euclid(360.0);
    assert!(diff > 0.9 && diff < 1.1);
}
```

**IMPORTANT NOTES:**

1. Always use `normalize_degrees()` to keep angles in 0-360 range
2. Convert to radians when using trigonometric functions
3. Use double precision (f64) throughout
4. Reference Meeus equation numbers in comments

#### 3.2.2 Implement `src/solar/sankranti.rs`

**Purpose:** Find exact time when Sun enters a zodiac sign

**Algorithm:** Newton-Raphson iteration

```rust
use crate::core::{JulianDay, constants::*};
use crate::solar::position::SolarCalculator;

/// Find Sankranti (Sun entering zodiac sign)
/// 
/// # Arguments
/// * `year` - BS year
/// * `month` - BS month (1-12)
/// 
/// # Returns
/// Julian Day when Sun enters corresponding zodiac sign
/// 
/// # Algorithm
/// Uses Newton-Raphson iteration to solve:
/// SunLongitude(t) = TargetLongitude
/// 
/// # Accuracy
/// ±10 seconds for simple mode
/// ±1 second for high-precision mode
pub fn find_sankranti(bs_year: i32, bs_month: u8) -> Result<JulianDay, AstroError> {
    // 1. Validate input
    if bs_month < 1 || bs_month > 12 {
        return Err(AstroError::InvalidMonth(bs_month));
    }
    
    // 2. Convert BS month to zodiac sign
    // Baisakh (month 1) = Aries (0°)
    // Jestha (month 2) = Taurus (30°)
    // etc.
    let zodiac_sign = bs_month - 1;
    let target_longitude = (zodiac_sign as f64) * ZODIAC_DEGREES;
    
    // 3. Initial guess: approximate date from BS year
    let ad_year_approx = bs_year - 57; // 2000 BS ≈ 1943 AD
    let ad_month_approx = bs_month as i32; // Rough approximation
    
    let mut jd = JulianDay::from_gregorian(
        ad_year_approx, 
        ad_month_approx as u8, 
        15, 
        0.0
    );
    
    // 4. Newton-Raphson iteration
    const MAX_ITERATIONS: usize = 20;
    const TOLERANCE: f64 = 1.0 / 86400.0; // 1 second in days
    
    for iteration in 0..MAX_ITERATIONS {
        let sun_long = SolarCalculator::apparent_longitude(jd);
        
        // Calculate angular difference (handle 360° wrap)
        let diff = angular_difference(target_longitude, sun_long);
        
        // Convergence check
        if diff.abs() < 0.001 { // 0.001° ≈ 2.4 seconds
            return Ok(jd);
        }
        
        // Sun moves ~0.985647° per day
        const SUN_DAILY_MOTION: f64 = 0.985647;
        let dt = diff / SUN_DAILY_MOTION;
        
        // Update Julian Day
        jd = jd.add_days(dt);
        
        // Safety check: shouldn't move more than 60 days
        if dt.abs() > 60.0 {
            return Err(AstroError::ConvergenceFailed);
        }
    }
    
    Err(AstroError::MaxIterationsExceeded)
}

/// Calculate angular difference accounting for 360° wrap
/// Returns value in range [-180, +180]
fn angular_difference(target: f64, current: f64) -> f64 {
    let diff = target - current;
    
    // Normalize to [-180, +180]
    if diff > 180.0 {
        diff - 360.0
    } else if diff < -180.0 {
        diff + 360.0
    } else {
        diff
    }
}

/// Error types for astronomical calculations
#[derive(Debug, Clone, thiserror::Error)]
pub enum AstroError {
    #[error("Invalid month: {0}")]
    InvalidMonth(u8),
    
    #[error("Convergence failed")]
    ConvergenceFailed,
    
    #[error("Maximum iterations exceeded")]
    MaxIterationsExceeded,
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_sankranti_2077_baisakh() {
        // 2077 Baisakh 1 (Mesh Sankranti) = April 13, 2020
        let jd = find_sankranti(2077, 1).unwrap();
        let (year, month, day, _) = jd.to_gregorian();
        
        assert_eq!(year, 2020);
        assert_eq!(month, 4);
        // Day should be 13 or 14 (depends on exact time)
        assert!(day >= 13 && day <= 14);
    }
    
    #[test]
    fn test_all_months_2077() {
        // All 12 months should have valid Sankranti
        for month in 1..=12 {
            let result = find_sankranti(2077, month);
            assert!(result.is_ok(), "Failed for month {}", month);
        }
    }
    
    #[test]
    fn test_angular_difference() {
        assert_eq!(angular_difference(10.0, 5.0), 5.0);
        assert_eq!(angular_difference(5.0, 10.0), -5.0);
        assert_eq!(angular_difference(10.0, 350.0), 20.0);
        assert_eq!(angular_difference(350.0, 10.0), -20.0);
    }
}
```

**CRITICAL RULES for Sankranti Finder:**

1. **Always handle 360° wrap** - Use `angular_difference()` function
2. **Limit iteration steps** - Prevent infinite loops
3. **Use good initial guess** - Within ±30 days of true date
4. **Check convergence** - Stop when accuracy achieved
5. **Validate results** - Ensure Sun actually at target longitude

### Phase 3: Lunar Calculations (Week 3)

**Priority: HIGH**

#### 3.3.1 Implement `src/lunar/position.rs`

**Mathematical Foundation:** Jean Meeus Chapter 47 (simplified)

**Required Functions:**

```rust
impl LunarCalculator {
    /// Mean longitude of Moon
    /// Reference: Meeus eq. 47.1
    pub fn mean_longitude(jd: JulianDay) -> f64 {
        let t = jd.centuries_since_j2000();
        
        // L' = 218.3164477° + 481267.88123421°T 
        //      - 0.0015786°T² + T³/538841 - T⁴/65194000
        
        let l = 218.3164477 
            + 481267.88123421 * t
            - 0.0015786 * t * t
            + t * t * t / 538841.0
            - t * t * t * t / 65194000.0;
        
        normalize_degrees(l)
    }
    
    /// Mean elongation of Moon
    /// Reference: Meeus eq. 47.2
    pub fn mean_elongation(jd: JulianDay) -> f64 {
        let t = jd.centuries_since_j2000();
        
        // D = 297.8501921° + 445267.1114034°T 
        //     - 0.0018819°T² + T³/545868 - T⁴/113065000
        
        let d = 297.8501921
            + 445267.1114034 * t
            - 0.0018819 * t * t
            + t * t * t / 545868.0
            - t * t * t * t / 113065000.0;
        
        normalize_degrees(d)
    }
    
    /// Mean anomaly of Moon
    /// Reference: Meeus eq. 47.4
    pub fn mean_anomaly(jd: JulianDay) -> f64 {
        let t = jd.centuries_since_j2000();
        
        // M' = 134.9633964° + 477198.8675055°T
        //      + 0.0087414°T² + T³/69699 - T⁴/14712000
        
        let m = 134.9633964
            + 477198.8675055 * t
            + 0.0087414 * t * t
            + t * t * t / 69699.0
            - t * t * t * t / 14712000.0;
        
        normalize_degrees(m)
    }
    
    /// Simplified true longitude of Moon
    /// Accuracy: ±2°
    /// For precise work, use full ELP-2000 theory
    pub fn true_longitude_simplified(jd: JulianDay) -> f64 {
        let l = Self::mean_longitude(jd);
        let d = Self::mean_elongation(jd) * DEG_TO_RAD;
        let m = Self::mean_anomaly(jd) * DEG_TO_RAD;
        let m_sun = crate::solar::SolarCalculator::mean_anomaly(jd) * DEG_TO_RAD;
        
        // Simplified perturbations (largest terms only)
        let correction = 
            6.288774 * m.sin()
            + 1.274027 * (2.0 * d - m).sin()
            + 0.658314 * (2.0 * d).sin()
            + 0.213618 * (2.0 * m).sin()
            - 0.185116 * m_sun.sin()
            - 0.114332 * (2.0 * d - 2.0 * m).sin();
        
        normalize_degrees(l + correction)
    }
}
```

**Validation Tests:**

```rust
#[test]
fn test_moon_j2000() {
    let jd = JulianDay(J2000_0);
    let longitude = LunarCalculator::mean_longitude(jd);
    // Moon's mean longitude at J2000.0 should be ~218.3°
    assert!((longitude - 218.3).abs() < 1.0);
}

#[test]
fn test_moon_moves_faster_than_sun() {
    let jd = JulianDay::from_gregorian(2020, 1, 1, 0.0);
    let long1 = LunarCalculator::true_longitude_simplified(jd);
    let long2 = LunarCalculator::true_longitude_simplified(jd.add_days(1.0));
    
    let moon_motion = (long2 - long1 + 360.0).rem_euclid(360.0);
    
    // Moon moves ~13° per day
    assert!(moon_motion > 11.0 && moon_motion < 15.0);
}
```

#### 3.3.2 Implement `src/lunar/tithi.rs`

**Purpose:** Calculate Tithi (lunar day)

```rust
/// Calculate Tithi at given Julian Day
/// 
/// Tithi is defined by elongation of Moon from Sun:
/// Tithi = floor((MoonLong - SunLong) / 12°) + 1
/// 
/// Returns: 1-30 (1-15 = Shukla Paksha, 16-30 = Krishna Paksha)
pub fn calculate_tithi(jd: JulianDay) -> u8 {
    let sun_long = SolarCalculator::apparent_longitude(jd);
    let moon_long = LunarCalculator::true_longitude_simplified(jd);
    
    // Elongation (Moon ahead of Sun)
    let elongation = (moon_long - sun_long + 360.0).rem_euclid(360.0);
    
    // Each tithi = 12° of elongation
    let tithi = (elongation / TITHI_DEGREES).floor() as u8 + 1;
    
    // Should be 1-30
    if tithi < 1 || tithi > 30 {
        return 1; // Safety fallback
    }
    
    tithi
}

/// Find when a specific Tithi starts
/// Returns Julian Day of Tithi beginning
pub fn find_tithi_start(bs_year: i32, bs_month: u8, tithi: u8) -> Result<JulianDay, AstroError> {
    if tithi < 1 || tithi > 30 {
        return Err(AstroError::InvalidTithi(tithi));
    }
    
    // Target elongation
    let target_elongation = (tithi as f64 - 1.0) * TITHI_DEGREES;
    
    // Initial guess: start of month
    let month_start = crate::solar::find_sankranti(bs_year, bs_month)?;
    let mut jd = month_start.add_days((tithi as f64 - 1.0) * 0.984); // ~1 day per tithi
    
    // Newton-Raphson iteration
    for _ in 0..20 {
        let sun_long = SolarCalculator::apparent_longitude(jd);
        let moon_long = LunarCalculator::true_longitude_simplified(jd);
        let elongation = (moon_long - sun_long + 360.0).rem_euclid(360.0);
        
        let diff = angular_difference(target_elongation, elongation);
        
        if diff.abs() < 0.01 {
            return Ok(jd);
        }
        
        // Moon-Sun relative motion: ~12.19° per day
        let dt = diff / 12.19;
        jd = jd.add_days(dt);
    }
    
    Err(AstroError::ConvergenceFailed)
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_tithi_range() {
        let jd = JulianDay::from_gregorian(2020, 4, 14, 0.0);
        let tithi = calculate_tithi(jd);
        assert!(tithi >= 1 && tithi <= 30);
    }
    
    #[test]
    fn test_tithi_progression() {
        // Tithi should increase over time
        let jd1 = JulianDay::from_gregorian(2020, 4, 14, 0.0);
        let jd2 = jd1.add_days(1.0);
        
        let t1 = calculate_tithi(jd1);
        let t2 = calculate_tithi(jd2);
        
        // Should advance by 0-2 tithis per day
        let diff = (t2 as i32 - t1 as i32 + 30) % 30;
        assert!(diff >= 0 && diff <= 2);
    }
}
```

### Phase 4: Calendar Logic (Week 4-5)

**Priority: MEDIUM**

#### 3.4.1 Implement `src/calendar/month_calculator.rs`

**Purpose:** Calculate BS month length using Sankranti times

```rust
/// Calculate number of days in BS month
/// 
/// Algorithm:
/// 1. Find Sankranti for month N (when Sun enters zodiac sign N)
/// 2. Find Sankranti for month N+1
/// 3. Days = floor(Sankranti[N+1] - Sankranti[N])
/// 
/// # Returns
/// Number of days (typically 29-32)
pub fn calculate_month_days(bs_year: i32, bs_month: u8) -> Result<u8, AstroError> {
    // Find start of this month
    let sankranti_start = find_sankranti(bs_year, bs_month)?;
    
    // Find start of next month
    let (next_year, next_month) = if bs_month == 12 {
        (bs_year + 1, 1)
    } else {
        (bs_year, bs_month + 1)
    };
    
    let sankranti_end = find_sankranti(next_year, next_month)?;
    
    // Calculate days
    let days = sankranti_end.diff_days(&sankranti_start);
    let days_int = days.round() as u8;
    
    // Sanity check
    if days_int < 29 || days_int > 32 {
        return Err(AstroError::InvalidMonthLength(days_int));
    }
    
    Ok(days_int)
}

/// Generate complete BS calendar for a year
pub fn generate_year_calendar(bs_year: i32) -> Result<[u8; 12], AstroError> {
    let mut calendar = [0u8; 12];
    
    for month in 1..=12 {
        calendar[(month - 1) as usize] = calculate_month_days(bs_year, month)?;
    }
    
    Ok(calendar)
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_month_length_range() {
        let days = calculate_month_days(2077, 1).unwrap();
        assert!(days >= 29 && days <= 32);
    }
    
    #[test]
    fn test_year_total_days() {
        let calendar = generate_year_calendar(2077).unwrap();
        let total: u32 = calendar.iter().map(|&d| d as u32).sum();
        
        // BS year should be 354-385 days
        assert!(total >= 354 && total <= 385);
    }
}
```

### Phase 5: Validation (Week 6)

**Priority: CRITICAL**

#### 3.5.1 Create Validation Framework

```rust
// tests/validation.rs

use npdatetime_astronomical::prelude::*;
use std::fs::File;
use std::io::{BufRead, BufReader};

/// Load known data from CSV
fn load_csv_data(path: &str) -> Vec<(i32, u8, u8)> {
    let file = File::open(path).unwrap();
    let reader = BufReader::new(file);
    
    let mut data = Vec::new();
    
    for line in reader.lines().skip(1) { // Skip header
        let line = line.unwrap();
        let parts: Vec<&str> = line.split(',').collect();
        
        let year: i32 = parts[0].parse().unwrap();
        let month: u8 = parts[1].parse().unwrap();
        let days: u8 = parts[2].parse().unwrap();
        
        data.push((year, month, days));
    }
    
    data
}

#[test]
fn validate_against_csv() {
    let csv_data = load_csv_data("../npdatetime/data/calendar_bs.csv");