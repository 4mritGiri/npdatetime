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
        npdatetime::NepaliDate::today()
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
