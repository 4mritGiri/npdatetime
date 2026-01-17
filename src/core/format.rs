//! Date formatting utilities for Nepali dates
//!
//! Provides strftime-style formatting with support for Nepali month names,
//! weekdays, and custom formatting patterns.

use crate::core::date::{NEPALI_MONTHS, NEPALI_MONTHS_UNICODE, NEPALI_WEEKDAYS, NepaliDate};

impl NepaliDate {
    /// Formats the date using a format string
    ///
    /// # Format Specifiers:
    /// - `%Y` - Four-digit year (e.g., 2077)
    /// - `%y` - Two-digit year (e.g., 77)
    /// - `%m` - Month as zero-padded decimal (01-12)
    /// - `%B` - Full month name in English (e.g., Baisakh)
    /// - `%b` - Abbreviated month name (first 3 letters)
    /// - `%d` - Day as zero-padded decimal (01-31)
    /// - `%e` - Day as space-padded decimal ( 1-31)
    /// - `%A` - Full weekday name (requires conversion to Gregorian)
    /// - `%%` - Literal % character
    ///
    /// # Examples:
    /// ```
    /// use npdatetime::NepaliDate;
    /// let date = NepaliDate::new(2077, 5, 19).unwrap();
    /// assert_eq!(date.format_date("%Y-%m-%d"), "2077-05-19");
    /// assert_eq!(date.format_date("%d %B %Y"), "19 Bhadra 2077");
    /// ```
    pub fn format_date(&self, format_str: &str) -> String {
        let mut result = String::new();
        let mut chars = format_str.chars().peekable();

        while let Some(ch) = chars.next() {
            if ch == '%' {
                if let Some(&next_ch) = chars.peek() {
                    chars.next(); // consume the format character
                    match next_ch {
                        'Y' => result.push_str(&self.year.to_string()),
                        'y' => result.push_str(&format!("{:02}", self.year % 100)),
                        'm' => result.push_str(&format!("{:02}", self.month)),
                        'B' => result.push_str(NEPALI_MONTHS[(self.month - 1) as usize]),
                        'b' => result.push_str(&NEPALI_MONTHS[(self.month - 1) as usize][..3]),
                        'd' => result.push_str(&format!("{:02}", self.day)),
                        'e' => result.push_str(&format!("{:2}", self.day)),
                        'A' => {
                            // Calculate weekday (requires conversion to Gregorian)
                            if let Ok((y, m, d)) = self.to_gregorian() {
                                let weekday = calculate_weekday(y, m, d);
                                result.push_str(NEPALI_WEEKDAYS[weekday]);
                            }
                        }
                        '%' => result.push('%'),
                        _ => {
                            // Unknown format specifier - keep as-is
                            result.push('%');
                            result.push(next_ch);
                        }
                    }
                } else {
                    result.push('%');
                }
            } else {
                result.push(ch);
            }
        }

        result
    }

    /// Formats the date in Unicode Devanagari script
    ///
    /// # Example:
    /// ```
    /// use npdatetime::NepaliDate;
    /// let date = NepaliDate::new(2077, 1, 1).unwrap();
    /// println!("{}", date.format_unicode()); // "१ बैशाख २०७७"
    /// ```
    pub fn format_unicode(&self) -> String {
        format!(
            "{} {} {}",
            to_devanagari_number(self.day as i32),
            NEPALI_MONTHS_UNICODE[(self.month - 1) as usize],
            to_devanagari_number(self.year)
        )
    }
}

/// Calculate weekday using Zeller's congruence (0 = Sunday, 6 = Saturday)
fn calculate_weekday(year: i32, month: u8, day: u8) -> usize {
    let mut y = year;
    let mut m = month as i32;

    // Adjust for Zeller's congruence (Jan=13, Feb=14 of previous year)
    if m < 3 {
        m += 12;
        y -= 1;
    }

    let q = day as i32;
    let k = y % 100;
    let j = y / 100;

    let h = (q + (13 * (m + 1)) / 5 + k + k / 4 + j / 4 + 5 * j) % 7;

    // Convert Zeller's output to standard (0=Sun, 1=Mon, ..., 6=Sat)
    ((h + 6) % 7) as usize
}

/// Convert a number to Devanagari numerals
fn to_devanagari_number(num: i32) -> String {
    const DEVANAGARI_DIGITS: [char; 10] = ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९'];

    num.to_string()
        .chars()
        .map(|c| {
            if let Some(digit) = c.to_digit(10) {
                DEVANAGARI_DIGITS[digit as usize]
            } else {
                c
            }
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_format_year() {
        let date = NepaliDate::new(2077, 5, 19).unwrap();
        assert_eq!(date.format_date("%Y"), "2077");
        assert_eq!(date.format_date("%y"), "77");
    }

    #[test]
    fn test_format_month() {
        let date = NepaliDate::new(2077, 5, 19).unwrap();
        assert_eq!(date.format_date("%m"), "05");
        assert_eq!(date.format_date("%B"), "Bhadra");
        assert_eq!(date.format_date("%b"), "Bha");
    }

    #[test]
    fn test_format_day() {
        let date = NepaliDate::new(2077, 5, 9).unwrap();
        assert_eq!(date.format_date("%d"), "09");
        assert_eq!(date.format_date("%e"), " 9");
    }

    #[test]
    fn test_format_combined() {
        let date = NepaliDate::new(2077, 5, 19).unwrap();
        assert_eq!(date.format_date("%Y-%m-%d"), "2077-05-19");
        assert_eq!(date.format_date("%d %B %Y"), "19 Bhadra 2077");
    }

    #[test]
    fn test_devanagari_numbers() {
        assert_eq!(to_devanagari_number(2077), "२०७७");
        assert_eq!(to_devanagari_number(1), "१");
        assert_eq!(to_devanagari_number(19), "१९");
    }

    #[test]
    fn test_weekday_calculation() {
        // 2020-09-04 was a Friday (index 5)
        let weekday = calculate_weekday(2020, 9, 4);
        assert_eq!(weekday, 5);
    }
}
