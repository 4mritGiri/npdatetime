use crate::astronomical::core::JulianDay;
use crate::astronomical::core::time::utc_to_npt;
use crate::astronomical::calendar::BsCalendar;
use crate::core::error::{NpdatetimeError, Result};
use std::fmt;

/// Represents a date in the astronomical Bikram Sambat calendar
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub struct BsDate {
    pub year: i32,
    pub month: u8,
    pub day: u8,
}

impl BsDate {
    /// Creates a new astronomical BS date
    pub fn new(year: i32, month: u8, day: u8) -> Result<Self> {
        if !(1..=12).contains(&month) {
            return Err(NpdatetimeError::InvalidDate(format!(
                "Month must be between 1 and 12, got {}",
                month
            )));
        }

        let cal = BsCalendar::new();
        let max_day = cal.calculate_month_days(year, month);
        if day < 1 || day > max_day {
            return Err(NpdatetimeError::InvalidDate(format!(
                "Day must be between 1 and {}, got {}",
                max_day, day
            )));
        }

        Ok(BsDate { year, month, day })
    }

    /// Convert Julian Day to BS Date
    pub fn from_julian_day(jd: JulianDay) -> Result<Self> {
        // Convert to Nepal Local Time
        let npt_jd = utc_to_npt(jd);
        let (g_year, g_month, g_day, _) = npt_jd.to_gregorian();

        // Approximate BS year. Most of the year, BS = G + 57.
        // Baisakh usually starts in April (4).
        let mut bs_year = g_year + 57;
        let cal = BsCalendar::new();
        
        use crate::astronomical::solar::sankranti::SankrantiFinder;
        // Search for Mesh Sankranti in the current Gregorian year
        let mesh_sankranti = SankrantiFinder::find_sankranti(0, JulianDay::from_gregorian(g_year, 4, 1, 0.0))
            .map_err(|e| NpdatetimeError::CalculationError(e))?;
        
        let mut npt_mesh_jd = utc_to_npt(mesh_sankranti.julian_day);
        
        if npt_jd.0.floor() < npt_mesh_jd.0.floor() {
            bs_year -= 1;
            let prev_mesh = SankrantiFinder::find_sankranti(0, JulianDay::from_gregorian(g_year - 1, 4, 1, 0.0))
                .map_err(|e| NpdatetimeError::CalculationError(e))?;
            npt_mesh_jd = utc_to_npt(prev_mesh.julian_day);
        }

        let mut remaining_days = (npt_jd.0.floor() - npt_mesh_jd.0.floor()) as i64;
        let mut bs_month = 1u8;
        
        let info = cal.get_year_info(bs_year).map_err(|e| NpdatetimeError::CalculationError(e))?;
        
        while bs_month <= 12 {
            let month_days = info.month_lengths[bs_month as usize - 1] as i64;
            if remaining_days >= month_days {
                remaining_days -= month_days;
                bs_month += 1;
            } else {
                break;
            }
        }

        if bs_month > 12 {
            // This case should theoretically not be hit if month_lengths are correct
            bs_year += 1;
            bs_month = 1;
        }

        Ok(BsDate {
            year: bs_year,
            month: bs_month,
            day: (remaining_days + 1) as u8,
        })
    }

    /// Convert BS Date to Julian Day (approximate to start of day in NPT)
    pub fn to_julian_day(&self) -> Result<JulianDay> {
        use crate::astronomical::solar::sankranti::SankrantiFinder;
        
        // CONSISTENCY: We use the same anchor logic as from_julian_day
        let mesh_sankranti = SankrantiFinder::find_sankranti(0, JulianDay::from_gregorian(self.year - 57, 4, 1, 0.0))
            .map_err(|e| NpdatetimeError::CalculationError(e))?;
        
        let npt_mesh_jd = utc_to_npt(mesh_sankranti.julian_day);
        let mut total_days = 0i64;
        
        let cal = BsCalendar::new();
        let info = cal.get_year_info(self.year).map_err(|e| NpdatetimeError::CalculationError(e))?;
        
        for m in 1..self.month {
            total_days += info.month_lengths[m as usize - 1] as i64;
        }
        
        total_days += (self.day - 1) as i64;
        
        // Start of the day in NPT
        let jd_npt = JulianDay(npt_mesh_jd.0.floor() + total_days as f64 + 0.5); // Use midday for better round-tripping
        
        // Convert back to UTC
        use crate::astronomical::core::time::npt_to_utc;
        Ok(npt_to_utc(jd_npt))
    }

    pub fn to_gregorian(&self) -> Result<(i32, u8, u8)> {
        let jd = self.to_julian_day()?;
        let (y, m, d, _) = jd.to_gregorian();
        Ok((y, m, d))
    }

    pub fn from_gregorian(year: i32, month: u8, day: u8) -> Result<Self> {
        let jd = JulianDay::from_gregorian(year, month, day, 12.0); // Midday
        Self::from_julian_day(jd)
    }
}

impl fmt::Display for BsDate {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}-{:02}-{:02}", self.year, self.month, self.day)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bs_date_creation() {
        let date = BsDate::new(2081, 1, 1).unwrap();
        assert_eq!(date.year, 2081);
        assert_eq!(date.month, 1);
        assert_eq!(date.day, 1);
    }

    #[test]
    fn test_conversion_round_trip() {
        let original = BsDate::new(2081, 1, 1).unwrap();
        let jd = original.to_julian_day().unwrap();
        let round_trip = BsDate::from_julian_day(jd).unwrap();
        assert_eq!(original, round_trip);
    }
    
    #[test]
    fn test_specific_date_2081_baisakh_1() {
        // 2081 Baisakh 1 is 2024-04-13
        let date = BsDate::from_gregorian(2024, 4, 13).unwrap();
        assert_eq!(date.year, 2081);
        assert_eq!(date.month, 1);
        assert_eq!(date.day, 1);
    }
}
