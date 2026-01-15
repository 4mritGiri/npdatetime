//! Tithi calculation (Lunar day)
//! 
//! Tithi is determined by the elongation of the Moon from the Sun.
//! Each Tithi corresponds to 12° of increasing elongation.

use crate::astronomical::core::{JulianDay, newton_raphson::NewtonRaphsonSolver};
use crate::astronomical::solar::vsop87::Vsop87Calculator;
use super::elp2000::Elp2000Calculator;

/// Tithi names in order
pub const TITHI_NAMES: [&str; 30] = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya",
];

/// Paksha (Lunar fortnight)
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Paksha {
    Shukla, // Waxing (Bright)
    Krishna, // Waning (Dark)
}

impl std::fmt::Display for Paksha {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Paksha::Shukla => write!(f, "Shukla"),
            Paksha::Krishna => write!(f, "Krishna"),
        }
    }
}

/// Information about a Tithi
#[derive(Debug, Clone, Copy)]
pub struct Tithi {
    pub index: u8, // 1 to 30
    pub paksha: Paksha,
    pub elongation: f64,
}

impl Tithi {
    pub fn name(&self) -> &str {
        TITHI_NAMES[self.index as usize - 1]
    }

    /// Create Tithi from elongation (0 to 360)
    pub fn from_elongation(elongation: f64) -> Self {
        let elongation = elongation.rem_euclid(360.0);
        let index = (elongation / 12.0).floor() as u8 + 1;
        let paksha = if index <= 15 { Paksha::Shukla } else { Paksha::Krishna };
        
        Self {
            index: index.min(30),
            paksha,
            elongation,
        }
    }
}

pub struct TithiCalculator;

impl TithiCalculator {
    /// Calculate the current Tithi at a given Julian Day
    pub fn get_tithi(jd: JulianDay) -> Tithi {
        let sun_long = Vsop87Calculator::sun_apparent_longitude(jd);
        let moon_long = Elp2000Calculator::apparent_longitude(jd);
        
        let elongation = (moon_long - sun_long).rem_euclid(360.0);
        Tithi::from_elongation(elongation)
    }

    /// Find the ending time (Julian Day) of a specific Tithi
    pub fn find_tithi_end(target_index: u8, approx_jd: JulianDay) -> Result<JulianDay, String> {
        let target_elongation = (target_index as f64) * 12.0;
        
        let f = |jd: f64| {
            let tithi = Self::get_tithi(JulianDay(jd));
            let mut diff = tithi.elongation - target_elongation;
            
            // Normalize to [-180, 180] for root finding
            diff = (diff + 180.0).rem_euclid(360.0) - 180.0;
            diff
        };

        let solver = NewtonRaphsonSolver::new(50, 1e-8);
        match solver.solve_numerical(f, approx_jd.0, 0.001) {
            Ok(jd_end) => Ok(JulianDay(jd_end)),
            Err(e) => Err(format!("Newton-Raphson failed: {:?}", e)),
        }
    }
}
