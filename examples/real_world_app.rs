use npdatetime::prelude::*;
use std::io::{self, Write};

fn main() -> Result<()> {
    println!("--- Nepali Date Converter ---");
    
    let today = NepaliDate::today()?;
    println!("Current Date: {} ({})", today, today.format("%d %B %Y"));
    println!("In Devanagari: {}", today.format_unicode());

    print!("\nEnter a BS date (YYYY-MM-DD) or press Enter for today: ");
    io::stdout().flush().unwrap();

    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    let input = input.trim();

    let target_date = if input.is_empty() {
        today
    } else {
        match NepaliDate::parse(input, "%Y-%m-%d") {
            Ok(d) => d,
            Err(e) => {
                println!("Error parsing date: {}", e);
                return Ok(());
            }
        }
    };

    let (y, m, d) = target_date.to_gregorian()?;
    println!("\nResults for {}:", target_date);
    println!("Gregorian (AD): {}-{:02}-{:02}", y, m, d);
    println!("Weekday: {}", target_date.format("%A"));
    
    #[cfg(feature = "astronomical")]
    {
        use npdatetime::astronomical::BsCalendar;
        let cal = BsCalendar::new();
        let days = cal.calculate_month_days(target_date.year, target_date.month);
        println!("This month has {} days (astronomical check)", days);
    }

    Ok(())
}
