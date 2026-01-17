use npdatetime::prelude::*;

fn main() -> Result<()> {
    let date = NepaliDate::new(2077, 5, 19)?;
    println!("Start date: {}", date);

    // Add 10 days
    let future = date.add_days(10)?;
    println!("10 days later: {}", future);

    // Add 365 days (a year)
    let year_later = date.add_days(365)?;
    println!("365 days later: {}", year_later);

    // Subtract 30 days
    let past = date.add_days(-30)?;
    println!("30 days ago: {}", past);

    // Check difference in days (requires conversion to AD usually)
    let ad1 = date.to_gregorian()?;
    let ad2 = year_later.to_gregorian()?;
    println!("AD Difference: {:?} to {:?}", ad1, ad2);

    Ok(())
}
