use npdatetime::prelude::*;

fn main() {
    println!("Testing Future Dates (> 2100 BS)");
    println!("================================\n");

    let future_year = 2105;
    let month = 1;
    let day = 1;

    println!(
        "Attempting to create NepaliDate for {}/{:02}/{:02}...",
        future_year, month, day
    );

    match NepaliDate::new(future_year, month, day) {
        Ok(date) => {
            println!("✅ Successfully created NepaliDate: {}", date);

            match date.to_gregorian() {
                Ok((gy, gm, gd)) => {
                    println!("AD Date: {}-{:02}-{:02}", gy, gm, gd);

                    // Round trip
                    let round_trip = NepaliDate::from_gregorian(gy, gm, gd).unwrap();
                    println!("Round trip BS: {}", round_trip);

                    if round_trip == date {
                        println!("✅ Round trip MATCHED!");
                    } else {
                        println!("❌ Round trip FAILED!");
                    }
                }
                Err(e) => println!("❌ Failed to convert to Gregorian: {}", e),
            }
        }
        Err(e) => println!("❌ Failed to create NepaliDate: {}", e),
    }
}
