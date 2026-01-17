//! Moon position (ELP-2000)
//!
//! Re-exports from the main ELP2000 calculator module

pub use super::elp2000::Elp2000Calculator as MoonCalculator;

// Convenience functions
use crate::astronomical::core::JulianDay;

/// Calculate Moon's geocentric longitude (in degrees)
pub fn moon_longitude(jd: JulianDay) -> f64 {
    super::elp2000::Elp2000Calculator::geocentric_longitude(jd)
}

/// Calculate Moon's apparent longitude (includes nutation)
pub fn moon_apparent_longitude(jd: JulianDay) -> f64 {
    super::elp2000::Elp2000Calculator::apparent_longitude(jd)
}

/// Calculate Moon's distance from Earth (in km)
pub fn moon_distance(jd: JulianDay) -> f64 {
    super::elp2000::Elp2000Calculator::distance(jd)
}
