fn main() {
    #[cfg(not(feature = "astronomical"))]
    {
        println!("Please run with --all-features to perform comparison.");
    }

    #[cfg(feature = "astronomical")]
    {
        use npdatetime::astronomical::BsDate;
        use npdatetime::prelude::*;

        println!(
            "{:<15} | {:<15} | {:<15} | Status",
            "Gregorian", "NepaliDate", "BsDate"
        );
        println!("{:-<15}-|-{:-<15}-|-{:-<15}-|-------", "", "", "");

        let test_dates = vec![
            (2024, 4, 13),  // Baisakh 1, 2081
            (2020, 9, 4),   // Bhadra 19, 2077
            (2026, 1, 22),  // Today
            (2026, 2, 22),  // Today
            (2026, 3, 22),  // Today
            (2026, 4, 22),  // Today
            (2026, 5, 22),  // Today
            (2026, 6, 22),  // Today
            (2026, 7, 22),  // Today
            (2026, 8, 22),  // Today
            (2026, 9, 22),  // Today
            (2026, 10, 22), // Today
            (2026, 11, 22), // Today
            (2026, 12, 22), // Today
            (2027, 1, 22),  // Today
            (2027, 2, 22),  // Today
            (2027, 3, 22),  // Today
            (2027, 4, 22),  // Today
            (2027, 5, 22),  // Today
            (2027, 6, 22),  // Today
            (2027, 7, 22),  // Today
            (2027, 8, 22),  // Today
            (2027, 9, 22),  // Today
            (2027, 10, 22), // Today
            (2027, 11, 22), // Today
            (2027, 12, 22), // Today
        ];

        for (y, m, d) in test_dates {
            let civil = NepaliDate::from_gregorian(y, m, d).unwrap();
            let astro = BsDate::from_gregorian(y, m, d).unwrap();

            let status = if civil.to_string() == astro.to_string() {
                "MATCH"
            } else {
                "DIFF"
            };

            println!(
                "{}-{:02}-{:02}     | {:<15} | {:<15} | {}",
                y, m, d, civil, astro, status
            );
        }
    }
}
