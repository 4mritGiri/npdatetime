use npdatetime::prelude::*;

fn main() -> Result<()> {
    // BS to AD
    let bs_date = NepaliDate::new(2081, 1, 1)?;
    let (ad_year, ad_month, ad_day) = bs_date.to_gregorian()?;
    println!("BS {} -> AD {}-{:02}-{:02}", bs_date, ad_year, ad_month, ad_day);

    // AD to BS
    let ad_date = (2024, 4, 13);
    let bs_converted = NepaliDate::from_gregorian(ad_date.0, ad_date.1, ad_date.2)?;
    println!("AD {}-{:02}-{:02} -> BS {}", ad_date.0, ad_date.1, ad_date.2, bs_converted);

    Ok(())
}