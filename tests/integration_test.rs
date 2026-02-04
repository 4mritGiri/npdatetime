use npdatetime::prelude::*;

#[cfg(any(feature = "lookup-tables", feature = "astronomical"))]
#[test]
fn test_public_api_date_creation() {
    // Test creating a valid date
    let date = NepaliDate::new(2081, 1, 1).expect("Should create valid date");
    assert_eq!(date.year, 2081);
    assert_eq!(date.month, 1);
    assert_eq!(date.day, 1);

    // Test invalid date (month out of range)
    let err = NepaliDate::new(2077, 13, 1);
    assert!(err.is_err());
}

#[cfg(any(feature = "lookup-tables", feature = "astronomical"))]
#[test]
fn test_public_api_conversion() {
    let bs_date = NepaliDate::new(2081, 1, 1).unwrap();
    let (g_year, g_month, g_day) = bs_date.to_gregorian().unwrap();

    // 2081-01-01 BS is 2024-04-13 AD
    assert_eq!(g_year, 2024);
    assert_eq!(g_month, 4);
    assert_eq!(g_day, 13);

    // Round trip
    let from_greg = NepaliDate::from_gregorian(2024, 4, 13).unwrap();
    assert_eq!(from_greg, bs_date);
}

#[cfg(any(feature = "lookup-tables", feature = "astronomical"))]
#[test]
fn test_public_api_formatting() {
    let date = NepaliDate::new(2081, 1, 1).unwrap();
    assert_eq!(date.format("%Y-%m-%d"), "2081-01-01");
}

#[cfg(any(feature = "lookup-tables", feature = "astronomical"))]
#[test]
fn test_public_api_fiscal_year() {
    let date = NepaliDate::new(2080, 4, 1).unwrap(); // Shrawan 1
    assert_eq!(date.fiscal_year(), "2080/81");

    let date_end = NepaliDate::new(2080, 3, 31).unwrap(); // Ashadh 31
    assert_eq!(date_end.fiscal_year(), "2079/80");
}
