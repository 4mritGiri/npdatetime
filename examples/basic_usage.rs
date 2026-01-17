use npdatetime::prelude::*;

fn main() -> Result<()> {
    // Create a date
    let date = NepaliDate::new(2081, 1, 1)?;
    println!("Nepali Date: {}", date);

    // Convert to Gregorian
    let (year, month, day) = date.to_gregorian()?;
    println!("Gregorian Date: {}-{:02}-{:02}", year, month, day);

    Ok(())
}
