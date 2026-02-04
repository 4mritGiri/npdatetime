//! Date parsing utilities for Nepali dates
//!
//! Provides strptime-like parsing for Nepali date strings.

use crate::core::date::{NEPALI_MONTHS, NepaliDate};
use crate::core::error::{NpdatetimeError, Result};

impl NepaliDate {
    /// Parses a date string into a NepaliDate using a format string
    ///
    /// # Format Specifiers:
    /// - `%Y` - Four-digit year (e.g., 2077)
    /// - `%m` - Month as decimal (01-12)
    /// - `%d` - Day as decimal (01-32)
    /// - `%B` - Full month name in English (e.g., Bhadra)
    /// - `%b` - Abbreviated month name (first 3 letters)
    ///
    /// # Examples:
    /// ```
    /// # use npdatetime::NepaliDate;
    /// # if cfg!(any(feature = "lookup-tables", feature = "astronomical")) {
    /// let date = NepaliDate::parse("2077-05-19", "%Y-%m-%d").unwrap();
    /// assert_eq!(date.year, 2077);
    /// assert_eq!(date.month, 5);
    /// assert_eq!(date.day, 19);
    /// # }
    /// ```
    pub fn parse(input: &str, format: &str) -> Result<Self> {
        let mut year: Option<i32> = None;
        let mut month: Option<u8> = None;
        let mut day: Option<u8> = None;

        let mut input_chars = input.chars().peekable();
        let mut format_chars = format.chars().peekable();

        while let Some(f) = format_chars.next() {
            if f == '%' {
                match format_chars.next() {
                    Some('Y') => {
                        let val = consume_digits(&mut input_chars, 4)?;
                        year = Some(val as i32);
                    }
                    Some('m') => {
                        let val = consume_digits(&mut input_chars, 2)?;
                        month = Some(val as u8);
                    }
                    Some('d') => {
                        let val = consume_digits(&mut input_chars, 2)?;
                        day = Some(val as u8);
                    }
                    Some('B') => {
                        let mut found = false;
                        for (idx, &m_name) in NEPALI_MONTHS.iter().enumerate() {
                            if peek_match(&mut input_chars, m_name) {
                                consume_match(&mut input_chars, m_name);
                                month = Some((idx + 1) as u8);
                                found = true;
                                break;
                            }
                        }
                        if !found {
                            return Err(NpdatetimeError::InvalidDate(
                                "Failed to parse month name".to_string(),
                            ));
                        }
                    }
                    Some('b') => {
                        let mut found = false;
                        for (idx, &m_name) in NEPALI_MONTHS.iter().enumerate() {
                            let short_name = &m_name[..3];
                            if peek_match(&mut input_chars, short_name) {
                                consume_match(&mut input_chars, short_name);
                                month = Some((idx + 1) as u8);
                                found = true;
                                break;
                            }
                        }
                        if !found {
                            return Err(NpdatetimeError::InvalidDate(
                                "Failed to parse abbreviated month name".to_string(),
                            ));
                        }
                    }
                    Some('%') => {
                        if input_chars.next() != Some('%') {
                            return Err(NpdatetimeError::InvalidDate(
                                "Literal % mismatch".to_string(),
                            ));
                        }
                    }
                    _ => {
                        return Err(NpdatetimeError::InvalidDate(
                            "Invalid format specifier".to_string(),
                        ));
                    }
                }
            } else if input_chars.next() != Some(f) {
                return Err(NpdatetimeError::InvalidDate(format!(
                    "Character mismatch: expected {}",
                    f
                )));
            }
        }

        match (year, month, day) {
            (Some(y), Some(m), Some(d)) => NepaliDate::new(y, m, d),
            _ => Err(NpdatetimeError::InvalidDate(
                "Missing year, month or day in format".to_string(),
            )),
        }
    }
}

fn consume_digits(it: &mut std::iter::Peekable<std::str::Chars>, count: usize) -> Result<u32> {
    let mut s = String::new();
    for _ in 0..count {
        if let Some(c) = it.next() {
            if c.is_ascii_digit() {
                s.push(c);
            } else {
                return Err(NpdatetimeError::InvalidDate(format!(
                    "Expected digit, got {}",
                    c
                )));
            }
        } else {
            return Err(NpdatetimeError::InvalidDate(
                "Unexpected end of input".to_string(),
            ));
        }
    }
    s.parse::<u32>()
        .map_err(|e| NpdatetimeError::InvalidDate(e.to_string()))
}

fn peek_match(it: &mut std::iter::Peekable<std::str::Chars>, target: &str) -> bool {
    let mut temp_it = it.clone();
    for target_c in target.chars() {
        if temp_it.next() != Some(target_c) {
            return false;
        }
    }
    true
}

fn consume_match(it: &mut std::iter::Peekable<std::str::Chars>, target: &str) {
    for _ in 0..target.chars().count() {
        it.next();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[cfg(any(feature = "lookup-tables", feature = "astronomical"))]
    #[test]
    fn test_parse_iso() {
        let date = NepaliDate::parse("2077-05-19", "%Y-%m-%d").unwrap();
        assert_eq!(date.year, 2077);
        assert_eq!(date.month, 5);
        assert_eq!(date.day, 19);
    }

    #[cfg(any(feature = "lookup-tables", feature = "astronomical"))]
    #[test]
    fn test_parse_month_name() {
        let date = NepaliDate::parse("19 Bhadra 2077", "%d %B %Y").unwrap();
        assert_eq!(date.year, 2077);
        assert_eq!(date.month, 5);
        assert_eq!(date.day, 19);
    }

    #[cfg(any(feature = "lookup-tables", feature = "astronomical"))]
    #[test]
    fn test_parse_abbrev_month() {
        let date = NepaliDate::parse("2077/Bha/19", "%Y/%b/%d").unwrap();
        assert_eq!(date.year, 2077);
        assert_eq!(date.month, 5);
        assert_eq!(date.day, 19);
    }

    #[test]
    fn test_parse_mismatch() {
        let res = NepaliDate::parse("2077-05-19", "%Y/%m/%d");
        assert!(res.is_err());
    }
}
