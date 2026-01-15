use npdatetime::prelude::*;

fn main() -> Result<()> {
    println!("Comparing Lookup vs Astronomical methods...");
    
    let year = 2081;
    let month = 1;

    // Lookup
    let lookup_days = NepaliDate::days_in_month(year, month)?;
    println!("Lookup: {} month {} has {} days", year, month, lookup_days);

    #[cfg(feature = "astronomical")]
    {
        let calc = AstronomicalCalendar::new();
        let astro_days = calc.calculate_month_days(year, month);
        println!("Astronomical: {} month {} has {} days", year, month, astro_days);
    }

    Ok(())
}
