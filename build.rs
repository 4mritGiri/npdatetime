// build.rs - Runs at compile time CSV → Rust conversion
use std::fs::File;
use std::io::Write;

fn main() {
    println!("cargo:rerun-if-changed=data/calendar_bs.csv");

    // Read CSV
    let mut reader = csv::Reader::from_path("data/calendar_bs.csv").unwrap();
    let mut data: Vec<(i32, u8, u8)> = Vec::new();

    for result in reader.records() {
        let record = result.unwrap();
        let year: i32 = record[0].parse().unwrap();
        for month in 1..=12 {
            let days: u8 = record[month as usize].parse().unwrap();
            data.push((year, month as u8, days));
        }
    }

    // Generate Rust code with embedded data
    let out_dir = std::env::var("OUT_DIR").unwrap();
    let dest_path = std::path::Path::new(&out_dir).join("calendar_data.rs");
    let mut f = File::create(&dest_path).unwrap();

    // Write as Rust const array
    writeln!(f, "const BS_CALENDAR_DATA: &[(i32, u8, u8)] = &[").unwrap();
    for (year, month, days) in data {
        writeln!(f, "    ({}, {}, {}),", year, month, days).unwrap();
    }
    writeln!(f, "];").unwrap();
}
