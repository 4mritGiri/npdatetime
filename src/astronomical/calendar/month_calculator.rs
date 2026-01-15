//! Solar month calculator for Bikram Sambat
//! 
//! Determines month lengths by finding the Gregorian dates of consecutive 
//! Sankrantis in Nepal Local Time (UTC+5:45).

use crate::astronomical::solar::sankranti::SankrantiFinder;
use crate::astronomical::core::time::utc_to_npt;

pub struct SolarMonthCalculator;

impl SolarMonthCalculator {
    /// Calculate the lengths of all 12 months for a given BS year
    /// 
    /// Returns a vector of 12 integers representing the number of days in each month
    /// (Baisakh, Jestha, ..., Chaitra)
    pub fn calculate_month_lengths(bs_year: i32) -> Result<Vec<u8>, String> {
        // Get Sankrantis for the current year
        let current_year_sankrantis = SankrantiFinder::find_all_in_year(bs_year)?;
        
        // Get Mesh Sankranti of the NEXT year to find Chaitra's length
        let next_year_mesh = SankrantiFinder::find_sankranti(0, 
            current_year_sankrantis[11].julian_day.add_days(25.0))?;
        
        let mut all_sankrantis = current_year_sankrantis;
        all_sankrantis.push(next_year_mesh);
        
        let mut lengths = Vec::with_capacity(12);
        
        for i in 0..12 {
            let start_jd = all_sankrantis[i].julian_day;
            let end_jd = all_sankrantis[i+1].julian_day;
            
            // Convert JDs to Nepal Local Time and get Gregorian dates
            let (start_y, start_m, start_d, _) = utc_to_npt(start_jd).to_gregorian();
            let (end_y, end_m, end_d, _) = utc_to_npt(end_jd).to_gregorian();
            
            // Calculate total days between these two Gregorian dates
            let length = Self::days_between_gregorian(
                (start_y, start_m, start_d),
                (end_y, end_m, end_d)
            );
            
            lengths.push(length as u8);
        }
        
        Ok(lengths)
    }

    /// Helper to calculate days between two Gregorian dates
    fn days_between_gregorian(start: (i32, u8, u8), end: (i32, u8, u8)) -> i64 {
        use crate::core::date::{gregorian_to_days};
        let start_days = gregorian_to_days(start.0, start.1, start.2);
        let end_days = gregorian_to_days(end.0, end.1, end.2);
        end_days - start_days
    }
}
