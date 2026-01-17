//! Leap month (Adhika Masa) detection
//!
//! Identifies intercalary lunar months by checking for lunar months (New Moon to New Moon)
//! that do not contain a solar transit (Sankranti).

use crate::astronomical::core::JulianDay;
use crate::astronomical::lunar::tithi::TithiCalculator;
use crate::astronomical::solar::sankranti::SankrantiFinder;

pub struct LeapMonthDetector;

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct AdhikaMasa {
    /// The BS month index (1-12) that is doubled
    pub month_index: u8,
    /// The Julian Day starting the Adhika Masa
    pub start_jd: JulianDay,
    /// The Julian Day ending the Adhika Masa
    pub end_jd: JulianDay,
}

impl LeapMonthDetector {
    /// Find all Adhika Masas in a given BS year
    pub fn find_adhika_masa(bs_year: i32) -> Result<Vec<AdhikaMasa>, String> {
        let mut results = Vec::new();

        // Get all Sankrantis for this year
        let sankrantis = SankrantiFinder::find_all_in_year(bs_year)?;

        // For each solar month, check if there are two New Moons
        for i in 0..11 {
            let start_s = sankrantis[i].julian_day;
            let end_s = sankrantis[i + 1].julian_day;

            if let Some(adhika) = Self::check_interval(i as u8 + 1, start_s, end_s)? {
                results.push(adhika);
            }
        }

        // Also check the last month (Chaitra)
        let next_mesh =
            SankrantiFinder::find_sankranti(0, sankrantis[11].julian_day.add_days(25.0))?;
        if let Some(adhika) =
            Self::check_interval(12, sankrantis[11].julian_day, next_mesh.julian_day)?
        {
            results.push(adhika);
        }

        Ok(results)
    }

    fn check_interval(
        month_idx: u8,
        start_s: JulianDay,
        end_s: JulianDay,
    ) -> Result<Option<AdhikaMasa>, String> {
        // Find the first New Moon after start_s
        let nm1 = TithiCalculator::find_next_new_moon(start_s)?;

        // If this New Moon is still before the next Sankranti, check the one after it
        if nm1.0 < end_s.0 {
            let nm2 = TithiCalculator::find_next_new_moon(nm1)?;

            // If the second New Moon is ALSO before the next Sankranti,
            // then the lunar month (nm1, nm2) is an Adhika Masa
            if nm2.0 < end_s.0 {
                return Ok(Some(AdhikaMasa {
                    month_index: month_idx,
                    start_jd: nm1,
                    end_jd: nm2,
                }));
            }
        }

        Ok(None)
    }
}
