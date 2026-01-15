//! VSOP87 simplified planetary theory for Sun position
//! 
//! Implements a reduced-term version of VSOP87 for calculating
//! Earth's heliocentric position and deriving Sun's geocentric position.
//! 
//! This implementation uses the most significant terms from VSOP87D
//! (heliocentric spherical coordinates) providing ~0.01° accuracy.

use crate::astronomical::core::{JulianDay, constants::*};

/// VSOP87 term: amplitude, phase, rate
#[derive(Debug, Clone, Copy)]
struct VsopTerm {
    amplitude: f64,
    phase: f64,
    rate: f64,
}

impl VsopTerm {
    const fn new(amplitude: f64, phase: f64, rate: f64) -> Self {
        Self { amplitude, phase, rate }
    }

    /// Evaluate this term at given Julian centuries
    fn eval(&self, t: f64) -> f64 {
        self.amplitude * (self.phase + self.rate * t).cos()
    }
}

// ============================================================================
// VSOP87 COEFFICIENTS FOR EARTH (SIMPLIFIED)
// ============================================================================
// These are the largest-amplitude terms from VSOP87D theory
// Units: longitude (radians), latitude (radians), radius (AU)

/// L0 terms for Earth's heliocentric longitude (largest terms)
const L0_TERMS: &[VsopTerm] = &[
    VsopTerm::new(1.75347045673, 0.0, 0.0),
    VsopTerm::new(0.03341656456, 4.66925680417, 6283.07584999140),
    VsopTerm::new(0.00034894275, 4.62610241759, 12566.15169998280),
    VsopTerm::new(0.00003417572, 2.82886579754, 3.52311834900),
    VsopTerm::new(0.00003497056, 2.74411783405, 5753.38488489680),
    VsopTerm::new(0.00003135899, 3.62767041756, 77713.77146812050),
    VsopTerm::new(0.00002676218, 4.41808345438, 7860.41939243920),
    VsopTerm::new(0.00002342691, 6.13516214446, 3930.20969621960),
    VsopTerm::new(0.00001273165, 2.03709657878, 529.69096509460),
    VsopTerm::new(0.00001324294, 0.74246341673, 11506.76976979360),
];

/// L1 terms for Earth's heliocentric longitude
const L1_TERMS: &[VsopTerm] = &[
    VsopTerm::new(6283.07584999140, 0.0, 0.0),
    VsopTerm::new(0.00206058863, 2.67823455584, 6283.07584999140),
    VsopTerm::new(0.00004303419, 2.63512650414, 12566.15169998280),
    VsopTerm::new(0.00000425264, 1.59046982018, 3.52311834900),
    VsopTerm::new(0.00000119261, 5.79557487799, 26.29831979980),
    VsopTerm::new(0.00000109186, 2.96588354409, 1577.34354244780),
];

/// L2 terms for Earth's heliocentric longitude
const L2_TERMS: &[VsopTerm] = &[
    VsopTerm::new(0.00052918870, 0.0, 0.0),
    VsopTerm::new(0.00008719837, 1.07209062925, 6283.07584999140),
    VsopTerm::new(0.00000308718, 0.27133618813, 12566.15169998280),
];

/// B0 terms for Earth's heliocentric latitude (largest terms)
const B0_TERMS: &[VsopTerm] = &[
    VsopTerm::new(0.00000279620, 3.19870156017, 84334.66158130829),
    VsopTerm::new(0.00000101643, 5.42248619256, 5507.55323866740),
    VsopTerm::new(0.00000080445, 3.88013204458, 5223.69391980220),
];

/// B1 terms for Earth's heliocentric latitude
const B1_TERMS: &[VsopTerm] = &[
    VsopTerm::new(0.00000227778, 3.41372504278, 6283.07584999140),
    VsopTerm::new(0.00000009721, 5.15233725915, 12566.15169998280),
];

/// R0 terms for Earth's radius vector (largest terms)
const R0_TERMS: &[VsopTerm] = &[
    VsopTerm::new(1.00013988784, 0.0, 0.0),
    VsopTerm::new(0.01670699632, 3.09846350258, 6283.07584999140),
    VsopTerm::new(0.00013956024, 3.05524609456, 12566.15169998280),
    VsopTerm::new(0.00003083720, 5.19846674381, 77713.77146812050),
    VsopTerm::new(0.00001628463, 1.17387558054, 5753.38488489680),
    VsopTerm::new(0.00001575572, 2.84685214877, 7860.41939243920),
    VsopTerm::new(0.00000924799, 5.45292235116, 11506.76976979360),
    VsopTerm::new(0.00000542439, 4.56409151453, 3930.20969621960),
];

/// R1 terms for Earth's radius vector
const R1_TERMS: &[VsopTerm] = &[
    VsopTerm::new(0.00103018607, 1.10748968172, 6283.07584999140),
    VsopTerm::new(0.00001721238, 1.06442300386, 12566.15169998280),
];

// ============================================================================
// CALCULATION FUNCTIONS
// ============================================================================

/// Calculate Earth's heliocentric longitude (in radians)
fn earth_heliocentric_longitude_rad(jd: JulianDay) -> f64 {
    let t = jd.centuries_since_j2000() / 10.0; // Convert to millennia for these coefficients
    
    let l0: f64 = L0_TERMS.iter().map(|term| term.eval(t)).sum();
    let l1: f64 = L1_TERMS.iter().map(|term| term.eval(t)).sum();
    let l2: f64 = L2_TERMS.iter().map(|term| term.eval(t)).sum();
    
    l0 + l1 * t + l2 * t * t
}

/// Calculate Earth's heliocentric latitude (in radians)
fn earth_heliocentric_latitude_rad(jd: JulianDay) -> f64 {
    let t = jd.centuries_since_j2000() / 10.0;
    
    let b0: f64 = B0_TERMS.iter().map(|term| term.eval(t)).sum();
    let b1: f64 = B1_TERMS.iter().map(|term| term.eval(t)).sum();
    
    b0 + b1 * t
}

/// Calculate Earth's radius vector (distance from Sun in AU)
fn earth_radius_vector(jd: JulianDay) -> f64 {
    let t = jd.centuries_since_j2000() / 10.0;
    
    let r0: f64 = R0_TERMS.iter().map(|term| term.eval(t)).sum();
    let r1: f64 = R1_TERMS.iter().map(|term| term.eval(t)).sum();
    
    r0 + r1 * t
}



/// Normalize angle to [0, 360) degrees
fn normalize_degrees(angle: f64) -> f64 {
    angle.rem_euclid(360.0)
}

// ============================================================================
// PUBLIC API
// ============================================================================

/// VSOP87 calculator for high-precision solar positions
pub struct Vsop87Calculator;

impl Vsop87Calculator {
    /// Calculate Earth's heliocentric longitude (in degrees)
    /// 
    /// This is Earth's ecliptic longitude as seen from the Sun
    pub fn earth_heliocentric_longitude(jd: JulianDay) -> f64 {
        let lon_rad = earth_heliocentric_longitude_rad(jd);
        normalize_degrees(lon_rad * RAD_TO_DEG)
    }

    /// Calculate Earth's heliocentric latitude (in degrees)
    /// 
    /// This is Earth's ecliptic latitude as seen from the Sun
    /// (usually very small, close to 0)
    pub fn earth_heliocentric_latitude(jd: JulianDay) -> f64 {
        let lat_rad = earth_heliocentric_latitude_rad(jd);
        lat_rad * RAD_TO_DEG
    }

    /// Calculate Earth-Sun distance (in AU)
    pub fn earth_sun_distance(jd: JulianDay) -> f64 {
        earth_radius_vector(jd)
    }

    /// Calculate Sun's geocentric longitude (in degrees)
    /// 
    /// This is the Sun's apparent position as seen from Earth.
    /// It's Earth's heliocentric longitude + 180°
    pub fn sun_geocentric_longitude(jd: JulianDay) -> f64 {
        let earth_lon = Self::earth_heliocentric_longitude(jd);
        normalize_degrees(earth_lon + 180.0)
    }

    /// Calculate Sun's true longitude (alias for geocentric longitude)
    /// 
    /// In Indian astronomy, this is called Sayana (tropical) longitude
    pub fn sun_true_longitude(jd: JulianDay) -> f64 {
        Self::sun_geocentric_longitude(jd)
    }

    /// Calculate nutation in longitude (simplified)
    /// 
    /// Returns correction to longitude in degrees
    fn nutation_longitude(jd: JulianDay) -> f64 {
        let t = jd.centuries_since_j2000();
        
        // Mean longitude of lunar ascending node
        let omega = 125.04 - 1934.136 * t;
        let omega_rad = omega * DEG_TO_RAD;
        
        // Simplified nutation formula
        -0.00569 - 0.00478 * omega_rad.sin()
    }

    /// Calculate Sun's apparent longitude (includes nutation and aberration)
    /// 
    /// This is the most accurate representation of Sun's position
    pub fn sun_apparent_longitude(jd: JulianDay) -> f64 {
        let true_lon = Self::sun_true_longitude(jd);
        let nutation_and_aberration = Self::nutation_longitude(jd);
        
        normalize_degrees(true_lon + nutation_and_aberration)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_earth_longitude_j2000() {
        let jd = JulianDay(J2000_0);
        let lon = Vsop87Calculator::earth_heliocentric_longitude(jd);
        
        // At J2000.0, Earth should be near 100° heliocentric longitude
        assert!((lon - 100.46).abs() < 1.0, "Earth longitude at J2000.0 = {}", lon);
    }

    #[test]
    fn test_sun_longitude_j2000() {
        let jd = JulianDay(J2000_0);
        let lon = Vsop87Calculator::sun_geocentric_longitude(jd);
        
        // Sun should be at Earth_lon + 180°, so around 280°
        assert!((lon - 280.46).abs() < 1.0, "Sun longitude at J2000.0 = {}", lon);
    }

    #[test]
    fn test_earth_sun_distance() {
        let jd = JulianDay(J2000_0);
        let dist = Vsop87Calculator::earth_sun_distance(jd);
        
        // Distance should be close to 1 AU
        assert!((dist - 1.0).abs() < 0.02, "Earth-Sun distance = {} AU", dist);
    }

    #[test]
    fn test_earth_latitude_near_zero() {
        let jd = JulianDay(J2000_0);
        let lat = Vsop87Calculator::earth_heliocentric_latitude(jd);
        
        // Earth's latitude should be very small (< 0.001°)
        assert!(lat.abs() < 0.001, "Earth latitude = {}°", lat);
    }

    #[test]
    fn test_vernal_equinox_2020() {
        // March 20, 2020, 03:50 UTC (vernal equinox)
        let jd = JulianDay::from_gregorian(2020, 3, 20, 3.833);
        let lon = Vsop87Calculator::sun_apparent_longitude(jd);
        
        // Sun should be very close to 0° at vernal equinox
        let diff = if lon > 180.0 { 360.0 - lon } else { lon };
        assert!(diff < 0.5, "Sun longitude at vernal equinox = {}°", lon);
    }

    #[test]
    fn test_angle_normalization() {
        assert_eq!(normalize_degrees(370.0), 10.0);
        assert_eq!(normalize_degrees(-10.0), 350.0);
        assert_eq!(normalize_degrees(720.0), 0.0);
    }
}
