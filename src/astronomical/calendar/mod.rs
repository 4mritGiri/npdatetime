//! Bikram Sambat astronomical calendar logic
//!
//! Combines solar and lunar calculations to provide the full structure of a BS year.

pub mod bs_date;
pub mod leap_month;
pub mod month_calculator;
pub mod synchronization;

pub use bs_date::BsDate;
pub use leap_month::{AdhikaMasa, LeapMonthDetector};
pub use month_calculator::SolarMonthCalculator;
pub use synchronization::{CalendarSynchronizer, MonthDetail};

/// Information about a full Bikram Sambat year
#[derive(Debug, Clone)]
pub struct YearInfo {
    pub bs_year: i32,
    /// Length of each month (12 entries)
    pub month_lengths: Vec<u8>,
    /// Any detected leap months in this year
    pub leap_months: Vec<AdhikaMasa>,
}

/// Main calendar calculator
pub struct BsCalendar;

impl BsCalendar {
    pub fn new() -> Self {
        BsCalendar {}
    }

    /// Get the structure of a given BS year
    pub fn get_year_info(&self, bs_year: i32) -> Result<YearInfo, String> {
        let month_lengths = SolarMonthCalculator::calculate_month_lengths(bs_year)?;
        let leap_months = LeapMonthDetector::find_adhika_masa(bs_year)?;

        Ok(YearInfo {
            bs_year,
            month_lengths,
            leap_months,
        })
    }

    /// Calculate month length astronomically
    pub fn calculate_month_days(&self, year: i32, month: u8) -> u8 {
        if month < 1 || month > 12 {
            return 0;
        }

        match self.get_year_info(year) {
            Ok(info) => info.month_lengths[month as usize - 1],
            Err(_) => 0, // Fallback or handle error
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_year_2081_structure() {
        let cal = BsCalendar::new();
        let info = cal.get_year_info(2081).unwrap();

        assert_eq!(info.bs_year, 2081);
        assert_eq!(info.month_lengths.len(), 12);

        // Baisakh 2081 (starting April 13, 2024)
        assert_eq!(info.month_lengths[0], 31);

        // Total days in a year should be 365 or 366
        let total_days: u32 = info.month_lengths.iter().map(|&x| x as u32).sum();
        assert!(total_days == 365 || total_days == 366);
    }

    #[test]
    fn test_adhika_masa_2077() {
        let cal = BsCalendar::new();
        let info = cal.get_year_info(2077).unwrap();

        // Print detected leap months for verification
        println!("Leap months detected in 2077: {}", info.leap_months.len());
        for lm in &info.leap_months {
            println!(
                "Leap month: index {}, JD: {}-{}",
                lm.month_index, lm.start_jd.0, lm.end_jd.0
            );
        }
    }
}
