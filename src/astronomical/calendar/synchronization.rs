//! Calendar synchronization utilities
//!
//! Aligns solar and lunar components and provides higher-level
//! date mapping functions.

use crate::astronomical::calendar::YearInfo;

pub struct CalendarSynchronizer;

impl CalendarSynchronizer {
    /// Maps a year info structure to a list of monthly data
    pub fn get_monthly_details(info: &YearInfo) -> Vec<MonthDetail> {
        let mut details = Vec::new();
        for (i, &len) in info.month_lengths.iter().enumerate() {
            let month_idx = i as u8 + 1;
            let is_adhika = info
                .leap_months
                .iter()
                .any(|lm| lm.month_index == month_idx);

            details.push(MonthDetail {
                month_index: month_idx,
                length: len,
                is_adhika,
            });
        }
        details
    }
}

#[derive(Debug, Clone)]
pub struct MonthDetail {
    pub month_index: u8,
    pub length: u8,
    pub is_adhika: bool,
}
