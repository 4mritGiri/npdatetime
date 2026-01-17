// npdatetime-rust bindings for JavaScript
// 
//  This file is part of npdatetime-rust.
// 
//  npdatetime-rust is free software: you can redistribute it and/or modify
//  it under the terms of the MIT License.
// 
//  npdatetime-rust is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  MIT License for more details.
// 
//  You should have received a copy of the MIT License
//  along with npdatetime-rust.  If not, see <https://opensource.org/licenses/MIT>.
// 
use wasm_bindgen::prelude::*;
use serde::{Deserialize, Serialize};

#[wasm_bindgen]
extern "C" {
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);
}

/// Nepali (Bikram Sambat) date for JavaScript
#[wasm_bindgen]
#[derive(Clone, Serialize, Deserialize)]
pub struct NepaliDate {
    #[wasm_bindgen(skip)]
    pub inner: npdatetime::NepaliDate,
}

#[wasm_bindgen]
impl NepaliDate {
    /// Create a new Nepali date
    /// 
    /// @param {number} year - Bikram Sambat year
    /// @param {number} month - Month (1-12)
    /// @param {number} day - Day of month
    /// @returns {NepaliDate} New NepaliDate instance
    /// 
    /// @example
    /// const date = new NepaliDate(2077, 5, 19);
    /// console.log(date.toString()); // "2077-05-19"
    #[wasm_bindgen(constructor)]
    pub fn new(year: i32, month: u8, day: u8) -> Result<NepaliDate, JsValue> {
        npdatetime::NepaliDate::new(year, month, day)
            .map(|inner| NepaliDate { inner })
            .map_err(|e| JsValue::from_str(&e.to_string()))
    }

    /// Convert to Gregorian (AD) date
    /// 
    /// @returns {Array<number>} [year, month, day]
    /// 
    /// @example
    /// const date = new NepaliDate(2077, 5, 19);
    /// const [year, month, day] = date.toGregorian();
    /// console.log(`${year}-${month}-${day}`); // "2020-9-4"
    #[wasm_bindgen(js_name = toGregorian)]
    pub fn to_gregorian(&self) -> Result<Vec<i32>, JsValue> {
        self.inner.to_gregorian()
            .map(|(y, m, d)| vec![y, m as i32, d as i32])
            .map_err(|e| JsValue::from_str(&e.to_string()))
    }

    /// Create NepaliDate from Gregorian (AD) date
    /// 
    /// @param {number} year - Gregorian year
    /// @param {number} month - Month (1-12)
    /// @param {number} day - Day of month
    /// @returns {NepaliDate} Converted Nepali date
    /// 
    /// @example
    /// const date = NepaliDate.fromGregorian(2020, 9, 4);
    /// console.log(date.toString()); // "2077-05-19"
    #[wasm_bindgen(js_name = fromGregorian)]
    pub fn from_gregorian(year: i32, month: u8, day: u8) -> Result<NepaliDate, JsValue> {
        npdatetime::NepaliDate::from_gregorian(year, month, day)
            .map(|inner| NepaliDate { inner })
            .map_err(|e| JsValue::from_str(&e.to_string()))
    }

    /// Get today's Nepali date
    /// 
    /// @returns {NepaliDate} Today's date in BS
    #[wasm_bindgen(js_name = today)]
    pub fn today() -> Result<NepaliDate, JsValue> {
        let now = js_sys::Date::new_0();
        let year = now.get_full_year() as i32;
        let month = (now.get_month() + 1) as u8;
        let day = now.get_date() as u8;
        
        npdatetime::NepaliDate::from_gregorian(year, month, day)
            .map(|inner| NepaliDate { inner })
            .map_err(|e| JsValue::from_str(&e.to_string()))
    }

    /// Format the date as a string
    /// 
    /// @param {string} format - Format string (strftime-style)
    /// @returns {string} Formatted date string
    /// 
    /// @example
    /// const date = new NepaliDate(2077, 5, 19);
    /// console.log(date.format("%d %B %Y")); // "19 Bhadra 2077"
    pub fn format(&self, format_str: &str) -> String {
        self.inner.format(format_str)
    }

    /// Add days to the date
    /// 
    /// @param {number} days - Number of days to add (can be negative)
    /// @returns {NepaliDate} New date after adding days
    #[wasm_bindgen(js_name = addDays)]
    pub fn add_days(&self, days: i32) -> Result<NepaliDate, JsValue> {
        self.inner.add_days(days)
            .map(|inner| NepaliDate { inner })
            .map_err(|e| JsValue::from_str(&e.to_string()))
    }

    /// Get the ordinal representation of the date (days since 1975-01-01 BS)
    #[wasm_bindgen(js_name = toOrdinal)]
    pub fn to_ordinal(&self) -> i32 {
        self.inner.to_ordinal()
    }

    /// Create NepaliDate from an ordinal
    #[wasm_bindgen(js_name = fromOrdinal)]
    pub fn from_ordinal(ordinal: i32) -> Result<NepaliDate, JsValue> {
        npdatetime::NepaliDate::from_ordinal(ordinal)
            .map(|inner| NepaliDate { inner })
            .map_err(|e| JsValue::from_str(&e.to_string()))
    }

    /// Get the Nepali Fiscal Year (e.g., "2080/81")
    #[wasm_bindgen(getter, js_name = fiscalYear)]
    pub fn fiscal_year(&self) -> String {
        self.inner.fiscal_year()
    }

    /// Get the fiscal quarter (1-4)
    #[wasm_bindgen(getter, js_name = fiscalQuarter)]
    pub fn fiscal_quarter(&self) -> u8 {
        self.inner.fiscal_quarter()
    }

    /// Format the date in Unicode Devanagari script
    #[wasm_bindgen(js_name = formatUnicode)]
    pub fn format_unicode(&self) -> String {
        self.inner.format_unicode()
    }

    /// Generate a visual month calendar
    #[wasm_bindgen(js_name = monthCalendar)]
    pub fn month_calendar(&self) -> String {
        self.inner.month_calendar()
    }

    /// Get the year
    #[wasm_bindgen(getter)]
    pub fn year(&self) -> i32 {
        self.inner.year
    }

    /// Get the month (1-12)
    #[wasm_bindgen(getter)]
    pub fn month(&self) -> u8 {
        self.inner.month
    }

    /// Get the day
    #[wasm_bindgen(getter)]
    pub fn day(&self) -> u8 {
        self.inner.day
    }

    /// String representation
    #[wasm_bindgen(js_name = toString)]
    pub fn to_string(&self) -> String {
        format!("{}", self.inner)
    }
}

/// Initialize WASM module
#[wasm_bindgen(start)]
pub fn init() {
    #[cfg(feature = "console_error_panic_hook")]
    console_error_panic_hook::set_once();
}
