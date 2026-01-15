//! ELP-2000 simplified lunar theory for Moon position
//! 
//! Implements a reduced-term version of ELP-2000 for calculating
//! geocentric position of the Moon. 
//! 
//! This implementation uses the fundamental arguments and most significant 
//! periodic terms to provide accuracy suitable for Tithi and eclipse calculations.

use crate::astronomical::core::{JulianDay, constants::*};

/// Multipliers for fundamental arguments (D, M, M', F)
#[derive(Debug, Clone, Copy)]
struct LunarTerm {
    d: i8,
    m: i8,
    m_prime: i8,
    f: i8,
    amplitude: f64,
}

impl LunarTerm {
    const fn new(d: i8, m: i8, m_prime: i8, f: i8, amplitude: f64) -> Self {
        Self { d, m, m_prime, f, amplitude }
    }
}

/// Periodic terms for Moon's longitude (unit: 1e-4 degrees)
/// Based on Meeus/Chapront (Simplified)
const LONG_TERMS: &[LunarTerm] = &[
    LunarTerm::new(0, 0, 1, 0, 62887.74),
    LunarTerm::new(2, 0, -1, 0, 12740.27),
    LunarTerm::new(2, 0, 0, 0, 6583.14),
    LunarTerm::new(0, 0, 2, 0, 2136.18),
    LunarTerm::new(0, 1, 0, 0, -1851.16),
    LunarTerm::new(0, 0, 0, 2, -1143.32),
    LunarTerm::new(2, 0, -2, 0, 587.93),
    LunarTerm::new(2, -1, -1, 0, 570.66),
    LunarTerm::new(2, 0, 1, 0, 533.22),
    LunarTerm::new(2, -1, 0, 0, 457.58),
    LunarTerm::new(0, 1, -1, 0, -409.28),
    LunarTerm::new(1, 0, 0, 0, -347.46),
    LunarTerm::new(0, 1, 1, 0, -303.83),
    LunarTerm::new(2, 0, 0, -2, 153.27),
    LunarTerm::new(2, 1, -1, 0, -125.28),
    LunarTerm::new(0, 0, 1, 2, -109.81),
    LunarTerm::new(4, 0, -1, 0, -106.75),
    LunarTerm::new(0, 0, 1, -2, 100.34),
    LunarTerm::new(4, 0, 0, 0, 85.48),
    LunarTerm::new(2, 1, 0, 0, -78.88),
    LunarTerm::new(0, 1, 0, 2, -69.53),
    LunarTerm::new(2, -1, -2, 0, 50.86),
    LunarTerm::new(2, 0, -1, 2, 48.22),
    LunarTerm::new(2, -1, 1, 0, -40.36),
    LunarTerm::new(1, 1, 0, 0, -37.51),
    LunarTerm::new(0, 1, 0, -2, 32.06),
];

/// Periodic terms for Moon's distance (unit: km)
const DIST_TERMS: &[LunarTerm] = &[
    LunarTerm::new(0, 0, 1, 0, -20905.355),
    LunarTerm::new(2, 0, -1, 0, -3699.111),
    LunarTerm::new(2, 0, 0, 0, -2955.962),
    LunarTerm::new(0, 0, 2, 0, -569.925),
    LunarTerm::new(2, 0, 1, 0, 108.743),
    LunarTerm::new(2, -1, -1, 0, -104.755),
];

/// Fundamental arguments of Moon's motion
#[derive(Debug, Clone, Copy)]
struct FundamentalArgs {
    l_prime: f64, // Mean longitude of Moon
    d: f64,       // Mean elongation of Moon (Moon - Sun)
    m: f64,       // Mean anomaly of Sun
    m_prime: f64, // Mean anomaly of Moon
    f: f64,       // Mean distance of Moon from its ascending node
}

impl FundamentalArgs {
    fn calculate(jd: JulianDay) -> Self {
        let t = jd.centuries_since_j2000();
        let t2 = t * t;
        let t3 = t * t * t;
        let t4 = t * t * t * t;

        // Meeus, Formulas 47.1 - 47.5
        let l_prime = 218.3164477 + 481267.88123421 * t - 0.0015786 * t2 + t3 / 538841.0 - t4 / 65194000.0;
        let d = 297.8501921 + 445267.1114034 * t - 0.0018819 * t2 + t3 / 545868.0 - t4 / 113065000.0;
        let m = 357.5291092 + 35999.0502909 * t - 0.0001536 * t2 + t3 / 24490000.0;
        let m_prime = 134.9633964 + 477198.8675055 * t + 0.0087414 * t2 + t3 / 69699.0 - t4 / 14712000.0;
        let f = 93.2720950 + 483202.0175233 * t - 0.0036539 * t2 - t3 / 3526000.0 + t4 / 863310000.0;

        Self {
            l_prime: l_prime.rem_euclid(360.0),
            d: d.rem_euclid(360.0),
            m: m.rem_euclid(360.0),
            m_prime: m_prime.rem_euclid(360.0),
            f: f.rem_euclid(360.0),
        }
    }
}

pub struct Elp2000Calculator;

impl Elp2000Calculator {
    /// Calculate Moon's geocentric longitude (in degrees)
    pub fn geocentric_longitude(jd: JulianDay) -> f64 {
        let args = FundamentalArgs::calculate(jd);
        let t = jd.centuries_since_j2000();
        let e = 1.0 - 0.002516 * t - 0.0000074 * t * t;

        let mut delta_l = 0.0;
        for term in LONG_TERMS {
            let arg = (term.d as f64 * args.d + term.m as f64 * args.m + 
                           term.m_prime as f64 * args.m_prime + term.f as f64 * args.f) * DEG_TO_RAD;
            
            let mut coeff = term.amplitude;
            // Correction for Sun's eccentricity (Meeus formula 47)
            if term.m == 1 || term.m == -1 {
                coeff *= e;
            } else if term.m == 2 || term.m == -2 {
                coeff *= e * e;
            }
            
            delta_l += coeff * arg.sin();
        }

        // Add additional corrections from planetary perturbations (Meeus p. 341)
        let a1 = (119.75 + 131.849 * t).rem_euclid(360.0) * DEG_TO_RAD;
        let a2 = (53.09 + 479264.290 * t).rem_euclid(360.0) * DEG_TO_RAD;
        let a3 = (313.45 + 481266.484 * t).rem_euclid(360.0) * DEG_TO_RAD;
        
        delta_l += 39.5 * a1.sin();
        delta_l += 31.8 * a2.sin();
        delta_l += 19.6 * a3.sin();

        (args.l_prime + delta_l / 10000.0).rem_euclid(360.0)
    }

    /// Calculate Moon's distance from Earth (in km)
    pub fn distance(jd: JulianDay) -> f64 {
        let args = FundamentalArgs::calculate(jd);
        let t = jd.centuries_since_j2000();
        let e = 1.0 - 0.002516 * t - 0.0000074 * t * t;

        let mut delta_r = 0.0;
        for term in DIST_TERMS {
            let arg = (term.d as f64 * args.d + term.m as f64 * args.m + 
                           term.m_prime as f64 * args.m_prime + term.f as f64 * args.f) * DEG_TO_RAD;
            
            let mut coeff = term.amplitude;
            if term.m == 1 || term.m == -1 {
                coeff *= e;
            } else if term.m == 2 || term.m == -2 {
                coeff *= e * e;
            }
            
            delta_r += coeff * arg.cos();
        }

        385000.56 + delta_r
    }

    /// Calculate Moon's apparent longitude (includes nutation)
    pub fn apparent_longitude(jd: JulianDay) -> f64 {
        let geo_long = Self::geocentric_longitude(jd);
        
        // Nutation in longitude (simplified, same as solar)
        let t = jd.centuries_since_j2000();
        let omega = 125.04 - 1934.136 * t;
        let omega_rad = omega * DEG_TO_RAD;
        let nutation = -0.00569 - 0.00478 * omega_rad.sin();
        
        (geo_long + nutation).rem_euclid(360.0)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_moon_longitude_j2000() {
        let jd = JulianDay(J2000_0);
        let lon = Elp2000Calculator::geocentric_longitude(jd);
        
        // At J2000.0, Moon should be near 218.31° (mean longitude)
        // With periodic terms, it should be within a reasonable range.
        assert!((lon - 218.31).abs() < 7.0, "Moon longitude at J2000.0 = {}", lon);
    }
}
