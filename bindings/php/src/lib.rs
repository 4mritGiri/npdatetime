use ext_php_rs::prelude::*;
use npdatetime::NepaliDate as CoreNepaliDate;

#[php_class]
#[derive(Debug, Clone)]
pub struct NepaliDate {
    inner: CoreNepaliDate,
}

#[php_impl]
impl NepaliDate {
    /// Create a new Nepali date
    pub fn __construct(year: i32, month: i64, day: i64) -> PhpResult<Self> {
        CoreNepaliDate::new(year, month as u8, day as u8)
            .map(|inner| Self { inner })
            .map_err(|e| PhpException::default(e.to_string()))
    }

    /// Convert to Gregorian (AD) date
    /// Returns an array [year, month, day]
    pub fn to_gregorian(&self) -> PhpResult<Vec<i64>> {
        self.inner
            .to_gregorian()
            .map(|(y, m, d)| vec![y as i64, m as i64, d as i64])
            .map_err(|e| PhpException::default(e.to_string()))
    }

    /// Create NepaliDate from Gregorian (AD) date
    #[php_static_method]
    pub fn from_gregorian(year: i32, month: i64, day: i64) -> PhpResult<Self> {
        CoreNepaliDate::from_gregorian(year, month as u8, day as u8)
            .map(|inner| Self { inner })
            .map_err(|e| PhpException::default(e.to_string()))
    }

    /// Get today's Nepali date
    #[php_static_method]
    pub fn today() -> PhpResult<Self> {
        CoreNepaliDate::today()
            .map(|inner| Self { inner })
            .map_err(|e| PhpException::default(e.to_string()))
    }

    /// Format the date as a string
    pub fn format(&self, format_str: &str) -> String {
        self.inner.format(format_str)
    }

    /// Get the year
    pub fn get_year(&self) -> i32 {
        self.inner.year
    }

    /// Get the month (1-12)
    pub fn get_month(&self) -> i64 {
        self.inner.month as i64
    }

    /// Get the day
    pub fn get_day(&self) -> i64 {
        self.inner.day as i64
    }

    /// String representation
    pub fn __to_string(&self) -> String {
        format!("{}", self.inner)
    }
}

#[php_module]
pub fn get_module(module: ModuleBuilder) -> ModuleBuilder {
    module
}
