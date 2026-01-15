//! Time conversion utilities
//! Handles conversions between different time scales

use super::constants::*;

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


/// Ayanamsha (Chitra Paksha/Lahiri) approximation for Nirayana calculations
pub fn get_ayanamsha(jd: JulianDay) -> f64 {
    let t = jd.centuries_since_j2000();
    // Lahiri Ayanamsha: 23° 51' 25.532" at J2000.0
    23.857092 + 1.396971 * t + 0.000308 * t * t
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