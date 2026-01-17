use npdatetime::prelude::*;

fn main() -> Result<()> {
    let date = NepaliDate::new(2081, 1, 1)?;

    println!("Standard: {}", date);
    println!("Formatted (%Y-%m-%d): {}", date.format("%Y-%m-%d"));
    println!("Formatted (%d %B %Y): {}", date.format("%d %B %Y"));

    Ok(())
}
