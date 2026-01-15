//! Example: Calculate Sankranti (Solar events)

use npdatetime::solar::sankranti::SankrantiFinder;
use npdatetime::NepaliDate;

fn main() {
    println!("Calculating Sankranti for BS 2081...\n");

    let year = 2081;
    
    match SankrantiFinder::find_all_in_year(year) {
        Ok(sankrantis) => {
            println!("{:<12} | {:<20} | {:<15}", "Zodiac Sign", "Gregorian Date", "Nepali Date");
            println!("{:-<12}-+-{:-<20}-+-{:-<15}", "", "", "");
            
            for s in sankrantis {
                let (y, m, d, h) = s.julian_day.to_gregorian();
                let ns = s.to_bs_date();
                
                println!("{:<12} | {:04}-{:02}-{:02} {:02}:{:02} | {}", 
                    s.sign_name(),
                    y, m, d,
                    h as u32,
                    ((h % 1.0) * 60.0) as u32,
                    ns
                );
            }
        },
        Err(e) => println!("Error: {}", e),
    }
}