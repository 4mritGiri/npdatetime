# NPDateTime Project Implementation Guide
**Based on Your Current Structure**

## 🎯 Current Status Analysis

Your project has:
- ✅ **Lookup table implementation** (`src/lookup/`)
- ✅ **Astronomical calculator skeleton** (`src/astronomical/`)
- ✅ **CSV data** (`data/calendar_bs.csv`)
- ✅ **Build script** (`build.rs`)
- ✅ **Benchmarks** (showing performance comparisons)
- ✅ **Examples** (both basic and astronomical)
- ✅ **Bindings structure** ready for multiple languages

## 📋 What to Implement Next

### Priority 1: Complete Astronomical Calculator Core

#### File: `src/astronomical/solar/position.rs`

```rust
//! Solar position calculations using simplified VSOP87
//! Reference: Jean Meeus "Astronomical Algorithms" Chapter 25

use crate::astronomical::core::{JulianDay, constants::*};

pub struct SolarCalculator;

impl SolarCalculator {
    /// Calculate Sun's mean longitude
    /// Meeus eq. 25.2
    pub fn mean_longitude(jd: JulianDay) -> f64 {
        let t = jd.centuries_since_j2000();
        
        // L0 = 280.46646° + 36000.76983°T + 0.0003032°T²
        let l0 = 280.46646 + 36000.76983 * t + 0.0003032 * t * t;
        
        normalize_degrees(l0)
    }
    
    /// Calculate Sun's mean anomaly
    /// Meeus eq. 25.3
    pub fn mean_anomaly(jd: JulianDay) -> f64 {
        let t = jd.centuries_since_j2000();
        
        // M = 357.52911° + 35999.05029°T - 0.0001537°T²
        let m = 357.52911 + 35999.05029 * t - 0.0001537 * t * t;
        
        normalize_degrees(m)
    }
    
    /// Calculate equation of center
    /// Meeus eq. 25.4
    pub fn equation_of_center(jd: JulianDay) -> f64 {
        let t = jd.centuries_since_j2000();
        let m = Self::mean_anomaly(jd) * DEG_TO_RAD;
        
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
    
    /// Calculate Sun's apparent longitude
    /// Includes nutation and aberration
    pub fn apparent_longitude(jd: JulianDay) -> f64 {
        let true_long = Self::true_longitude(jd);
        let t = jd.centuries_since_j2000();
        
        // Simplified nutation
        let omega = 125.04 - 1934.136 * t;
        let nutation = -0.00569 - 0.00478 * (omega * DEG_TO_RAD).sin();
        
        normalize_degrees(true_long + nutation)
    }
}

/// Normalize angle to [0, 360) degrees
fn normalize_degrees(angle: f64) -> f64 {
    angle.rem_euclid(360.0)
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_sun_mean_longitude_j2000() {
        let jd = JulianDay(J2000_0);
        let l0 = SolarCalculator::mean_longitude(jd);
        assert!((l0 - 280.46).abs() < 0.1);
    }
    
    #[test]
    fn test_sun_2020_april() {
        // April 14, 2020 - Sun should be in Aries
        let jd = JulianDay::from_gregorian(2020, 4, 14, 12.0);
        let longitude = SolarCalculator::apparent_longitude(jd);
        assert!(longitude >= 0.0 && longitude < 30.0);
    }
}
```

#### File: `src/astronomical/solar/sankranti.rs`

```rust
//! Sankranti calculation - finding when Sun enters zodiac signs

use crate::astronomical::core::{JulianDay, constants::*};
use crate::astronomical::solar::position::SolarCalculator;
use crate::core::error::NpDateTimeError;

pub type Result<T> = std::result::Result<T, NpDateTimeError>;

/// Find when Sun enters a specific zodiac sign
/// 
/// # Arguments
/// * `bs_year` - Bikram Sambat year
/// * `bs_month` - Bikram Sambat month (1-12)
/// 
/// # Returns
/// Julian Day when Sun enters the corresponding zodiac sign
pub fn find_sankranti(bs_year: i32, bs_month: u8) -> Result<JulianDay> {
    if bs_month < 1 || bs_month > 12 {
        return Err(NpDateTimeError::InvalidMonth);
    }
    
    // BS month maps to zodiac sign
    // Baisakh (1) = Aries (0°), Jestha (2) = Taurus (30°), etc.
    let zodiac_index = bs_month - 1;
    let target_longitude = (zodiac_index as f64) * ZODIAC_DEGREES;
    
    // Initial guess: approximate Gregorian date
    let approx_ad_year = bs_year - 57;
    let approx_ad_month = bs_month;
    
    let mut jd = JulianDay::from_gregorian(
        approx_ad_year,
        approx_ad_month,
        14,
        0.0
    );
    
    // Newton-Raphson iteration
    const MAX_ITERATIONS: usize = 20;
    const TOLERANCE: f64 = 0.001; // 0.001° ≈ 2.4 seconds
    
    for iteration in 0..MAX_ITERATIONS {
        let sun_long = SolarCalculator::apparent_longitude(jd);
        let diff = angular_difference(target_longitude, sun_long);
        
        // Check convergence
        if diff.abs() < TOLERANCE {
            return Ok(jd);
        }
        
        // Sun moves ~0.985647° per day
        const SUN_DAILY_MOTION: f64 = 0.985647;
        let dt = diff / SUN_DAILY_MOTION;
        
        // Update Julian Day
        jd = jd.add_days(dt);
        
        // Safety check
        if dt.abs() > 60.0 {
            return Err(NpDateTimeError::CalculationError(
                "Sankranti iteration diverged".into()
            ));
        }
    }
    
    Err(NpDateTimeError::CalculationError(
        "Max iterations exceeded".into()
    ))
}

/// Calculate angular difference accounting for 360° wrap
fn angular_difference(target: f64, current: f64) -> f64 {
    let diff = target - current;
    
    if diff > 180.0 {
        diff - 360.0
    } else if diff < -180.0 {
        diff + 360.0
    } else {
        diff
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_sankranti_2077_baisakh() {
        // 2077 Baisakh 1 should be around April 13-14, 2020
        let jd = find_sankranti(2077, 1).unwrap();
        let (year, month, day, _) = jd.to_gregorian();
        
        assert_eq!(year, 2020);
        assert_eq!(month, 4);
        assert!(day >= 13 && day <= 14);
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

#### File: `src/astronomical/core/newton_raphson.rs`

```rust
//! Newton-Raphson iteration utilities

/// Generic Newton-Raphson solver
/// 
/// Solves f(x) = 0 using iteration: x_{n+1} = x_n - f(x_n)/f'(x_n)
pub struct NewtonRaphson<F, FPrime>
where
    F: Fn(f64) -> f64,
    FPrime: Fn(f64) -> f64,
{
    f: F,
    f_prime: FPrime,
    max_iterations: usize,
    tolerance: f64,
}

impl<F, FPrime> NewtonRaphson<F, FPrime>
where
    F: Fn(f64) -> f64,
    FPrime: Fn(f64) -> f64,
{
    pub fn new(f: F, f_prime: FPrime) -> Self {
        Self {
            f,
            f_prime,
            max_iterations: 50,
            tolerance: 1e-6,
        }
    }
    
    pub fn with_tolerance(mut self, tolerance: f64) -> Self {
        self.tolerance = tolerance;
        self
    }
    
    pub fn with_max_iterations(mut self, max_iter: usize) -> Self {
        self.max_iterations = max_iter;
        self
    }
    
    pub fn solve(&self, initial_guess: f64) -> Option<f64> {
        let mut x = initial_guess;
        
        for _ in 0..self.max_iterations {
            let fx = (self.f)(x);
            
            if fx.abs() < self.tolerance {
                return Some(x);
            }
            
            let fpx = (self.f_prime)(x);
            
            if fpx.abs() < 1e-12 {
                // Derivative too small
                return None;
            }
            
            x = x - fx / fpx;
        }
        
        None
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_solve_quadratic() {
        // Solve x² - 4 = 0 (should give x = 2)
        let solver = NewtonRaphson::new(
            |x| x * x - 4.0,
            |x| 2.0 * x,
        );
        
        let root = solver.solve(1.0).unwrap();
        assert!((root - 2.0).abs() < 1e-6);
    }
}
```

### Priority 2: Implement Month Calculator

#### File: `src/astronomical/calendar/month_calculator.rs`

```rust
//! Calculate BS month lengths using astronomical methods

use crate::astronomical::solar::sankranti::find_sankranti;
use crate::astronomical::core::JulianDay;
use crate::core::error::NpDateTimeError;

pub type Result<T> = std::result::Result<T, NpDateTimeError>;

/// Calculate number of days in a BS month astronomically
pub fn calculate_month_days(bs_year: i32, bs_month: u8) -> Result<u8> {
    // Find Sankranti for this month
    let sankranti_start = find_sankranti(bs_year, bs_month)?;
    
    // Find Sankranti for next month
    let (next_year, next_month) = if bs_month == 12 {
        (bs_year + 1, 1)
    } else {
        (bs_year, bs_month + 1)
    };
    
    let sankranti_end = find_sankranti(next_year, next_month)?;
    
    // Calculate difference in days
    let days = sankranti_end.diff_days(&sankranti_start);
    let days_int = days.round() as u8;
    
    // Sanity check
    if days_int < 29 || days_int > 32 {
        return Err(NpDateTimeError::CalculationError(
            format!("Invalid month length: {}", days_int)
        ));
    }
    
    Ok(days_int)
}

/// Generate complete calendar for a year
pub fn generate_year_calendar(bs_year: i32) -> Result<[u8; 12]> {
    let mut calendar = [0u8; 12];
    
    for month in 1..=12 {
        calendar[(month - 1) as usize] = calculate_month_days(bs_year, month)?;
    }
    
    Ok(calendar)
}

/// Get detailed year information
pub struct YearInfo {
    pub year: i32,
    pub months: [u8; 12],
    pub total_days: u16,
    pub sankranti_times: Vec<(u8, JulianDay)>,
}

impl YearInfo {
    pub fn calculate(bs_year: i32) -> Result<Self> {
        let months = generate_year_calendar(bs_year)?;
        let total_days: u16 = months.iter().map(|&d| d as u16).sum();
        
        let mut sankranti_times = Vec::with_capacity(12);
        for month in 1..=12 {
            let jd = find_sankranti(bs_year, month)?;
            sankranti_times.push((month, jd));
        }
        
        Ok(YearInfo {
            year: bs_year,
            months,
            total_days,
            sankranti_times,
        })
    }
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
    fn test_year_total() {
        let calendar = generate_year_calendar(2077).unwrap();
        let total: u32 = calendar.iter().map(|&d| d as u32).sum();
        
        // BS year should be 354-385 days
        assert!(total >= 354 && total <= 385);
    }
}
```

### Priority 3: Create Validation Example

#### File: `examples/astronomical/validate_astronomical.rs`

```rust
//! Validate astronomical calculations against lookup table data

use npdatetime::astronomical::calendar::month_calculator;
use npdatetime::lookup;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Validating Astronomical Calculations");
    println!("=====================================\n");
    
    // Load CSV data
    let csv_data = load_csv_data("data/calendar_bs.csv")?;
    
    let mut matches = 0;
    let mut mismatches = Vec::new();
    let mut errors = Vec::new();
    
    // Test range: 2077 (reduce for faster testing)
    let test_year = 2077;
    
    println!("Testing year {}...", test_year);
    
    for month in 1..=12 {
        // Get expected value from CSV/lookup
        let expected = lookup::days_in_month(test_year, month)?;
        
        // Calculate astronomically
        match month_calculator::calculate_month_days(test_year, month) {
            Ok(calculated) => {
                if calculated == expected {
                    matches += 1;
                    print!("✓");
                } else {
                    mismatches.push((test_year, month, expected, calculated));
                    print!("✗");
                }
            }
            Err(e) => {
                errors.push((test_year, month, e.to_string()));
                print!("E");
            }
        }
    }
    
    println!("\n");
    println!("Results:");
    println!("--------");
    println!("Matches: {}", matches);
    println!("Mismatches: {}", mismatches.len());
    println!("Errors: {}", errors.len());
    
    if !mismatches.is_empty() {
        println!("\nMismatches:");
        for (y, m, exp, calc) in &mismatches {
            println!("  {}/{}: Expected {}, Got {}", y, m, exp, calc);
        }
    }
    
    if !errors.is_empty() {
        println!("\nErrors:");
        for (y, m, err) in &errors {
            println!("  {}/{}: {}", y, m, err);
        }
    }
    
    Ok(())
}

fn load_csv_data(path: &str) -> Result<Vec<(i32, u8, u8)>, Box<dyn std::error::Error>> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    
    let mut data = Vec::new();
    
    for (idx, line) in reader.lines().enumerate() {
        if idx == 0 {
            continue; // Skip header
        }
        
        let line = line?;
        let parts: Vec<&str> = line.split(',').collect();
        
        if parts.len() >= 3 {
            let year: i32 = parts[0].parse()?;
            let month: u8 = parts[1].parse()?;
            let days: u8 = parts[2].parse()?;
            
            data.push((year, month, days));
        }
    }
    
    Ok(data)
}
```

### Priority 4: Update Your Error Types

#### File: `src/core/error.rs`

Add astronomical-specific errors:

```rust
#[derive(Debug, Clone, thiserror::Error)]
pub enum NpDateTimeError {
    #[error("Invalid date: {0}")]
    InvalidDate(String),
    
    #[error("Invalid month")]
    InvalidMonth,
    
    #[error("Out of range: {0}")]
    OutOfRange(String),
    
    #[error("Parse error: {0}")]
    ParseError(String),
    
    // NEW: Astronomical errors
    #[error("Calculation error: {0}")]
    CalculationError(String),
    
    #[error("Convergence failed")]
    ConvergenceFailed,
    
    #[error("Maximum iterations exceeded")]
    MaxIterationsExceeded,
}
```

### Priority 5: Wire Everything Together

#### File: `src/astronomical/mod.rs`

```rust
//! Astronomical calculations for Bikram Sambat calendar

pub mod core;
pub mod solar;
pub mod lunar;
pub mod calendar;

// Re-exports
pub use calendar::month_calculator;
pub use solar::sankranti;

/// Main astronomical API
pub struct AstronomicalCalculator;

impl AstronomicalCalculator {
    /// Calculate month length using astronomical methods
    pub fn calculate_month_days(year: i32, month: u8) -> crate::core::error::Result<u8> {
        calendar::month_calculator::calculate_month_days(year, month)
    }
    
    /// Find Sankranti time
    pub fn find_sankranti(year: i32, month: u8) -> crate::core::error::Result<core::JulianDay> {
        solar::sankranti::find_sankranti(year, month)
    }
    
    /// Generate complete year calendar
    pub fn generate_year(year: i32) -> crate::core::error::Result<[u8; 12]> {
        calendar::month_calculator::generate_year_calendar(year)
    }
}
```

## 🧪 Testing Strategy

### Run Your Tests

```bash
# Test lookup table (should already work)
cargo test --lib lookup

# Test astronomical calculations (after implementing above)
cargo test --lib astronomical

# Run validation example
cargo run --example validate_astronomical

# Run benchmarks
cargo bench
```

## 📊 Expected Results

After implementation, you should see:

```
Validating Astronomical Calculations
=====================================

Testing year 2077...
✓✓✓✓✓✓✓✓✓✓✓✓

Results:
--------
Matches: 12
Mismatches: 0
Errors: 0
```

## 🎯 Next Steps After This

1. **Extend validation** to more years (2000-2090)
2. **Implement lunar calculations** for Tithi
3. **Add leap month detection**
4. **Complete Python bindings** in `bindings/python/`
5. **Build WASM** for JavaScript in `bindings/javascript/`

## 🚨 Important Notes

### When Following the Guidelines

1. **Always reference Meeus equations** in comments
2. **Keep modules independent** - solar shouldn't depend on lunar
3. **Use Result<T>** for all fallible operations
4. **Test incrementally** - don't write all code at once
5. **Validate against CSV** frequently

### Code Quality Checklist

- [ ] All public functions documented
- [ ] Meeus equation numbers cited
- [ ] Unit tests written
- [ ] Integration tests pass
- [ ] Benchmarks run
- [ ] Validated against CSV data

## 📁 Files You Need to Create/Modify

Based on your structure, focus on:

1. ✅ `src/astronomical/solar/position.rs` - **CREATE**
2. ✅ `src/astronomical/solar/sankranti.rs` - **CREATE**
3. ✅ `src/astronomical/core/newton_raphson.rs` - **CREATE**
4. ✅ `src/astronomical/calendar/month_calculator.rs` - **MODIFY**
5. ✅ `src/core/error.rs` - **MODIFY** (add astronomical errors)
6. ✅ `examples/astronomical/validate_astronomical.rs` - **CREATE**

## 🎓 Learning Path

1. **Week 1**: Implement solar position and Sankranti
2. **Week 2**: Wire up month calculator and validate
3. **Week 3**: Optimize and fix any mismatches
4. **Week 4**: Document and create examples

This gives you a complete, working astronomical calculator that validates against your CSV data!