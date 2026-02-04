use npdatetime::prelude::*;

#[test]
fn test_public_api_date_creation() {
    // Test creating a valid date
    let date = NepaliDate::new(2077, 5, 19).expect("Should create valid date");
    assert_eq!(date.year, 2077);
    assert_eq!(date.month, 5);
    assert_eq!(date.day, 19);

    // Test invalid date (month out of range)
    let err = NepaliDate::new(2077, 13, 1);
    assert!(err.is_err());
}

#[test]
fn test_public_api_conversion() {
    let bs_date = NepaliDate::new(2077, 5, 19).unwrap();
    let (g_year, g_month, g_day) = bs_date.to_gregorian().unwrap();

    // 2077-05-19 BS is 2020-09-04 AD
    assert_eq!(g_year, 2020);
    assert_eq!(g_month, 9);
    assert_eq!(g_day, 4);

    // Round trip
    let from_greg = NepaliDate::from_gregorian(2020, 9, 4).unwrap();
    assert_eq!(from_greg, bs_date);
}

#[test]
fn test_public_api_formatting() {
    let date = NepaliDate::new(2077, 5, 19).unwrap();
    assert_eq!(date.format("%Y-%m-%d"), "2077-05-19");
}

#[test]
fn test_public_api_fiscal_year() {
    let date = NepaliDate::new(2080, 4, 1).unwrap(); // Shrawan 1
    assert_eq!(date.fiscal_year(), "2080/81");

    let date_end = NepaliDate::new(2080, 3, 31).unwrap(); // Ashadh 31
    assert_eq!(date_end.fiscal_year(), "2079/80");
}
