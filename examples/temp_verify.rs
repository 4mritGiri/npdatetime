use npdatetime::prelude::*;
use npdatetime::astronomical::calendar::BsCalendar;

fn main() -> Result<()> {
    let cal = BsCalendar::new();
    let info = cal.get_year_info(2082).map_err(|e| NpdatetimeError::CalculationError(e))?;
    println!("Astro 2082 Month Lengths: {:?}", info.month_lengths);
    let total: u32 = info.month_lengths.iter().map(|&x| x as u32).sum();
    println!("Total Days: {}", total);
    
    // Check lookup lengths
    let lookup_lengths: Vec<u8> = (1..=12).map(|m| NepaliDate::days_in_month(2082, m).unwrap()).collect();
    println!("Lookup 2082 Month Lengths: {:?}", lookup_lengths);
    
    Ok(())
}
