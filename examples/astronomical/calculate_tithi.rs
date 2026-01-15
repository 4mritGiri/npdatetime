use npdatetime::core::JulianDay;
use npdatetime::lunar::tithi::TithiCalculator;

fn main() {
    println!("Tithi Calculation for January 15, 2026...\n");

    // Julian Day for Jan 15, 2026, 12:00 UTC
    let jd = JulianDay::from_gregorian(2026, 1, 15, 12.0);
    
    let tithi = TithiCalculator::get_tithi(jd);
    println!("Current Tithi: {} ({})", tithi.name(), tithi.paksha);
    println!("Elongation: {:.2}°", tithi.elongation);

    // Find when this Tithi ends
    match TithiCalculator::find_tithi_end(tithi.index, jd) {
        Ok(end_jd) => {
            let (y, m, d, h) = end_jd.to_gregorian();
            println!("Tithi Ends at: {:04}-{:02}-{:02} {:02}:{:02} UTC", 
                y, m, d, h as u32, ((h % 1.0) * 60.0) as u32);
        },
        Err(e) => println!("Error finding Tithi end: {}", e),
    }

    // List upcoming Tithis
    println!("\nUpcoming Tithis:");
    let mut current_jd = jd;
    for _ in 0..5 {
        let t = TithiCalculator::get_tithi(current_jd);
        match TithiCalculator::find_tithi_end(t.index, current_jd) {
            Ok(next_jd) => {
                let (y, m, d, h) = next_jd.to_gregorian();
                println!("{:<12} ends at {:04}-{:02}-{:02} {:02}:{:02} UTC", 
                    t.name(), y, m, d, h as u32, ((h % 1.0) * 60.0) as u32);
                current_jd = JulianDay(next_jd.0 + 0.1);
            },
            Err(_) => break,
        }
    }
}