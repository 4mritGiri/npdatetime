//! Sun position calculations
//! Uses simplified VSOP87 or full precision depending on features

use crate::astronomical::core::{JulianDay, constants::*};

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
