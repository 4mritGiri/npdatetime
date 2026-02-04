use npdatetime::prelude::*;

fn main() -> Result<()> {
    #[cfg(not(feature = "astronomical"))]
    {
        println!("Please run with --all-features to perform comparison.");
    }

    #[cfg(feature = "astronomical")]
    {
        println!("Comparing Astronomical vs Lookup (1975 - 2100 BS)...");
        let cal = AstronomicalCalendar::new();
        let mut discrepancies = 0;
        let mut total_months = 0;

        for year in 1975..=2100 {
            let info = cal
                .get_year_info(year)
                .map_err(NpdatetimeError::ParseError)?;

            for month in 1..=12 {
                total_months += 1;
                let lookup_val = NepaliDate::days_in_month(year, month as u8)?;
                let astro_val = info.month_lengths[month - 1];

                if lookup_val != astro_val {
                    discrepancies += 1;
                    if discrepancies <= 10 {
                        println!(
                            "Discrepancy at {}-{:02}: Lookup={}, Astro={}",
                            year, month, lookup_val, astro_val
                        );
                    }
                }
            }
        }

        println!("\nVerification Complete.");
        println!("Total Months Checked: {}", total_months);
        println!("Total Discrepancies: {}", discrepancies);
        println!(
            "Accuracy: {:.2}%",
            (1.0 - (discrepancies as f64 / total_months as f64)) * 100.0
        );

        if discrepancies > 0 {
            println!("\nNote: Minor discrepancies are expected due to floating-point precision ");
            println!("and different Lahiri Ayanamsha approximations used in various sources.");
        }
    }

    Ok(())
}
