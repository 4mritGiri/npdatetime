use crate::core::error::{NpdatetimeError, Result};
use std::fmt;

// Reference point: Start of BS 1975
pub const BS_EPOCH_YEAR: i32 = 1975;
pub const BS_EPOCH_AD: (i32, u8, u8) = (1918, 4, 13);

/// Month names in Nepali
pub const NEPALI_MONTHS: [&str; 12] = [
    "Baisakh", "Jestha", "Ashadh", "Shrawan", "Bhadra", "Ashwin",
    "Kartik", "Mangsir", "Poush", "Magh", "Falgun", "Chaitra",
];

/// Month names in Nepali (Devanagari)
pub const NEPALI_MONTHS_UNICODE: [&str; 12] = [
    "बैशाख", "जेष्ठ", "आषाढ", "श्रावण", "भाद्र", "आश्विन",
    "कार्तिक", "मंसिर", "पौष", "माघ", "फाल्गुन", "चैत्र",
];

/// Weekday names in Nepali
pub const NEPALI_WEEKDAYS: [&str; 7] = [
    "Aaitabaar", "Sombaar", "Mangalbaar", "Budhabaar",
    "Bihibaar", "Shukrabaar", "Shanibaar",
];

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub struct NepaliDate {
    pub year: i32,
    pub month: u8,
    pub day: u8,
}

impl NepaliDate {
    /// Creates a new Nepali date
    pub fn new(year: i32, month: u8, day: u8) -> Result<Self> {
        if month < 1 || month > 12 {
            return Err(NpdatetimeError::InvalidDate(
                format!("Month must be between 1 and 12, got {}", month)
            ));
        }

        let max_day = Self::days_in_month(year, month)?;
        if day < 1 || day > max_day {
            return Err(NpdatetimeError::InvalidDate(
                format!("Day must be between 1 and {}, got {}", max_day, day)
            ));
        }

        Ok(NepaliDate { year, month, day })
    }

    /// Returns the number of days in a given month
    pub fn days_in_month(year: i32, month: u8) -> Result<u8> {
        if month < 1 || month > 12 {
            return Err(NpdatetimeError::InvalidDate(
                format!("Invalid month: {}", month)
            ));
        }

        // Access the lookup data. 
        // Note: For now, we'll keep the lookup logic here or in a dedicated lookup module.
        // In the final lib.rs, we'll probably have a way to access BS_MONTH_DATA.
        // For now, let's assume we'll use a trait or a global provided by lib.rs 
        // (but that creates circular dependencies).
        // Let's keep it simple for now and move the data access to lib.rs or a dedicated lookup mod.
        
        crate::lookup::get_days_in_month(year, month)
    }

    /// Converts Nepali date to Gregorian date (year, month, day)
    pub fn to_gregorian(&self) -> Result<(i32, u8, u8)> {
        let mut total_days = 0i64;

        for y in BS_EPOCH_YEAR..self.year {
            for m in 1..=12 {
                total_days += Self::days_in_month(y, m)? as i64;
            }
        }

        for m in 1..self.month {
            total_days += Self::days_in_month(self.year, m)? as i64;
        }

        total_days += (self.day - 1) as i64;

        let (mut year, mut month, mut day) = BS_EPOCH_AD;
        let mut days_to_add = total_days;

        while days_to_add > 0 {
            let days_in_current_month = gregorian_days_in_month(year, month);
            if days_to_add >= (days_in_current_month - day + 1) as i64 {
                days_to_add -= (days_in_current_month - day + 1) as i64;
                day = 1;
                month += 1;
                if month > 12 {
                    month = 1;
                    year += 1;
                }
            } else {
                day += days_to_add as u8;
                days_to_add = 0;
            }
        }

        Ok((year, month, day))
    }

    /// Creates a Nepali date from a Gregorian date
    pub fn from_gregorian(year: i32, month: u8, day: u8) -> Result<Self> {
        let total_days = gregorian_days_since_epoch(year, month, day, BS_EPOCH_AD)?;

        let mut remaining_days = total_days;
        let mut bs_year = BS_EPOCH_YEAR;
        let mut bs_month = 1u8;

        loop {
            let mut year_days = 0;
            for m in 1..=12 {
                year_days += Self::days_in_month(bs_year, m)? as i64;
            }

            if remaining_days >= year_days {
                remaining_days -= year_days;
                bs_year += 1;
            } else {
                break;
            }
        }

        while bs_month <= 12 {
            let month_days = Self::days_in_month(bs_year, bs_month)? as i64;
            if remaining_days >= month_days {
                remaining_days -= month_days;
                bs_month += 1;
            } else {
                break;
            }
        }

        let bs_day = (remaining_days + 1) as u8;
        Self::new(bs_year, bs_month, bs_day)
    }

    /// Returns today's date in Nepali calendar
    pub fn today() -> Result<Self> {
        use std::time::{SystemTime, UNIX_EPOCH};
        
        let duration = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap();
        
        let days_since_unix_epoch = duration.as_secs() / 86400;
        let (year, month, day) = unix_epoch_to_gregorian(days_since_unix_epoch);
        
        Self::from_gregorian(year, month, day)
    }

    /// Formats the date as a string
    pub fn format(&self, format_str: &str) -> String {
        format_str
            .replace("%Y", &self.year.to_string())
            .replace("%m", &format!("{:02}", self.month))
            .replace("%d", &format!("{:02}", self.day))
            .replace("%B", NEPALI_MONTHS[(self.month - 1) as usize])
            .replace("%b", &NEPALI_MONTHS[(self.month - 1) as usize][..3])
    }

    /// Adds days to the date
    pub fn add_days(&self, days: i32) -> Result<Self> {
        let (g_year, g_month, g_day) = self.to_gregorian()?;
        let total_days = gregorian_to_days(g_year, g_month, g_day) + days as i64;
        let (new_year, new_month, new_day) = days_to_gregorian(total_days);
        Self::from_gregorian(new_year, new_month, new_day)
    }
}

impl fmt::Display for NepaliDate {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}-{:02}-{:02}", self.year, self.month, self.day)
    }
}

// Gregorian helpers (keeping them here for now, could go to utils)

pub fn is_gregorian_leap_year(year: i32) -> bool {
    (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)
}

pub fn gregorian_days_in_month(year: i32, month: u8) -> u8 {
    match month {
        1 | 3 | 5 | 7 | 8 | 10 | 12 => 31,
        4 | 6 | 9 | 11 => 30,
        2 => if is_gregorian_leap_year(year) { 29 } else { 28 },
        _ => 0,
    }
}

pub fn gregorian_days_since_epoch(
    year: i32,
    month: u8,
    day: u8,
    epoch: (i32, u8, u8),
) -> Result<i64> {
    let (ey, em, ed) = epoch;
    
    if year < ey || (year == ey && month < em) 
        || (year == ey && month == em && day < ed) {
        return Err(NpdatetimeError::OutOfRange(
            "Date is before the BS epoch".to_string()
        ));
    }

    let mut total_days = 0i64;

    for y in ey..year {
        total_days += if is_gregorian_leap_year(y) { 366 } else { 365 };
    }

    for m in 1..em {
        total_days -= gregorian_days_in_month(ey, m) as i64;
    }
    total_days -= (ed - 1) as i64;

    for m in 1..month {
        total_days += gregorian_days_in_month(year, m) as i64;
    }
    total_days += (day - 1) as i64;

    Ok(total_days)
}

pub fn gregorian_to_days(year: i32, month: u8, day: u8) -> i64 {
    let mut days = 0i64;
    for y in 1..year {
        days += if is_gregorian_leap_year(y) { 366 } else { 365 };
    }
    for m in 1..month {
        days += gregorian_days_in_month(year, m) as i64;
    }
    days + day as i64
}

pub fn days_to_gregorian(mut days: i64) -> (i32, u8, u8) {
    let mut year = 1i32;
    loop {
        let year_days = if is_gregorian_leap_year(year) { 366 } else { 365 };
        if days > year_days {
            days -= year_days;
            year += 1;
        } else {
            break;
        }
    }
    let mut month = 1u8;
    while month <= 12 {
        let month_days = gregorian_days_in_month(year, month) as i64;
        if days > month_days {
            days -= month_days;
            month += 1;
        } else {
            break;
        }
    }
    (year, month, days as u8)
}

pub fn unix_epoch_to_gregorian(days_since_epoch: u64) -> (i32, u8, u8) {
    let base_days = gregorian_to_days(1970, 1, 1);
    let total_days = base_days + days_since_epoch as i64;
    days_to_gregorian(total_days)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_valid_date() {
        let date = NepaliDate::new(2077, 5, 19).unwrap();
        assert_eq!(date.year, 2077);
        assert_eq!(date.month, 5);
        assert_eq!(date.day, 19);
    }

    #[test]
    fn test_invalid_month() {
        assert!(NepaliDate::new(2077, 13, 1).is_err());
        assert!(NepaliDate::new(2077, 0, 1).is_err());
    }

    #[test]
    fn test_conversion_to_gregorian() {
        let bs_date = NepaliDate::new(2000, 1, 1).unwrap();
        let ad_date = bs_date.to_gregorian().unwrap();
        assert_eq!(ad_date, (1943, 4, 14));
    }

    #[test]
    fn test_conversion_from_gregorian() {
        let bs_date = NepaliDate::from_gregorian(1943, 4, 14).unwrap();
        assert_eq!(bs_date.year, 2000);
        assert_eq!(bs_date.month, 1);
        assert_eq!(bs_date.day, 1);
    }

    #[test]
    fn test_format() {
        let date = NepaliDate::new(2077, 5, 19).unwrap();
        assert_eq!(date.format("%Y-%m-%d"), "2077-05-19");
        assert_eq!(date.format("%d %B %Y"), "19 Bhadra 2077");
    }

    #[test]
    fn test_display() {
        let date = NepaliDate::new(2077, 5, 19).unwrap();
        assert_eq!(format!("{}", date), "2077-05-19");
    }
}
