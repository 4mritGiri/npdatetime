//! Sankranti (Solar Transit) calculation
//! 
//! Finds when the Sun enters different zodiac signs using Newton-Raphson method
//! and high-precision VSOP87 solar position.

use crate::astronomical::core::{JulianDay, newton_raphson::NewtonRaphsonSolver, time::get_ayanamsha};
use super::vsop87::Vsop87Calculator;
use crate::NepaliDate;

/// Information about a Sankranti event
#[derive(Debug, Clone, Copy)]
pub struct Sankranti {
    /// The zodiac sign the Sun enters
    pub zodiac_sign: u8, // 0 to 11
    /// Julian Day of the transit
    pub julian_day: JulianDay,
}

impl Sankranti {
    /// Get the name of the zodiac sign
    pub fn sign_name(&self) -> &'static str {
        match self.zodiac_sign {
            0 => "Mesh",
            1 => "Vrishabha",
            2 => "Mithuna",
            3 => "Karka",
            4 => "Simha",
            5 => "Kanya",
            6 => "Tula",
            7 => "Vrishchika",
            8 => "Dhanu",
            9 => "Makara",
            10 => "Kumbha",
            11 => "Meena",
            _ => "Unknown",
        }
    }

    /// Convert to BS date
    pub fn to_bs_date(&self) -> NepaliDate {
        let (y, m, d, _) = self.julian_day.to_gregorian();
        NepaliDate::from_gregorian(y, m, d).unwrap_or(NepaliDate { year: 0, month: 0, day: 0 })
    }
}

pub struct SankrantiFinder;

impl SankrantiFinder {
    /// Find when the Sun enters a specific zodiac sign
    /// 
    /// # Arguments
    /// * `target_sign` - Zodiac sign index (0-11)
    /// * `approx_jd` - Approximate Julian Day to start searching from
    pub fn find_sankranti(target_sign: u8, approx_jd: JulianDay) -> Result<Sankranti, String> {
        let target_long = (target_sign as f64) * 30.0;
        
        // Function to find root for: nirayana_sun_longitude(jd) - target_long = 0
        let f = |jd: f64| {
            let julian_day = JulianDay(jd);
            let sayana_long = Vsop87Calculator::sun_apparent_longitude(julian_day);
            let ayanamsha = get_ayanamsha(julian_day);
            let nirayana_long = (sayana_long - ayanamsha).rem_euclid(360.0);
            
            // println!("JD: {}, Sayana: {}, Ay: {}, Nirayana: {}", jd, sayana_long, ayanamsha, nirayana_long);
            
            let mut diff = nirayana_long - target_long;
            
            // Normalize difference to [-180, 180] for root finding
            diff = (diff + 180.0).rem_euclid(360.0) - 180.0;
            diff
        };

        let solver = NewtonRaphsonSolver::new(50, 1e-8);
        
        // Use numerical derivative for simplicity (h = 0.001 days is about 1.4 minutes)
        match solver.solve_numerical(f, approx_jd.0, 0.0001) {
            Ok(root_jd) => Ok(Sankranti {
                zodiac_sign: target_sign,
                julian_day: JulianDay(root_jd),
            }),
            Err(e) => Err(format!("Sankranti calculation failed: {}", e)),
        }
    }

    /// Find all Sankrantis in a given BS year
    pub fn find_all_in_year(bs_year: i32) -> Result<Vec<Sankranti>, String> {
        let mut results = Vec::new();
        
        // Mesh Sankranti 2081 is around April 13, 2024
        // Approximate year in Gregorian: bs_year - 57
        let approx_greg_year = bs_year - 57;
        let mut current_search_jd = JulianDay::from_gregorian(approx_greg_year, 4, 1, 0.0);

        for sign in 0..12 {
            let sankranti = Self::find_sankranti(sign as u8, current_search_jd)?;
            results.push(sankranti);
            // Move search point forward by ~30 days for next sign
            current_search_jd = JulianDay(sankranti.julian_day.0 + 25.0);
        }

        Ok(results)
    }
}
