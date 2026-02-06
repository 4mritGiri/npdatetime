use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;

/// Nepali (Bikram Sambat) date representation
#[pyclass]
#[derive(Clone)]
struct NepaliDate {
    inner: npdatetime_core::NepaliDate,
}

#[pymethods]
impl NepaliDate {
    /// Create a new Nepali date
    /// 
    /// Args:
    ///     year (int): Bikram Sambat year
    ///     month (int): Month (1-12)
    ///     day (int): Day of month
    /// 
    /// Returns:
    ///     NepaliDate: A new NepaliDate instance
    /// 
    /// Example:
    ///     >>> from npdatetime import NepaliDate
    ///     >>> date = NepaliDate(2077, 5, 19)
    ///     >>> print(date)
    ///     2077-05-19
    #[new]
    fn new(year: i32, month: u8, day: u8) -> PyResult<Self> {
        npdatetime_core::NepaliDate::new(year, month, day)
            .map(|inner| NepaliDate { inner })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    /// Convert to Gregorian (AD) date
    /// 
    /// Returns:
    ///     tuple: (year, month, day) as integers
    /// 
    /// Example:
    ///     >>> date = NepaliDate(2077, 5, 19)
    ///     >>> date.to_gregorian()
    ///     (2020, 9, 4)
    fn to_gregorian(&self) -> PyResult<(i32, u8, u8)> {
        self.inner.to_gregorian()
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    /// Create NepaliDate from Gregorian (AD) date
    /// 
    /// Args:
    ///     year (int): Gregorian year
    ///     month (int): Month (1-12)
    ///     day (int): Day of month
    /// 
    /// Returns:
    ///     NepaliDate: Converted Nepali date
    /// 
    /// Example:
    ///     >>> date = NepaliDate.from_gregorian(2020, 9, 4)
    ///     >>> print(date)
    ///     2077-05-19
    #[staticmethod]
    fn from_gregorian(year: i32, month: u8, day: u8) -> PyResult<Self> {
        npdatetime_core::NepaliDate::from_gregorian(year, month, day)
            .map(|inner| NepaliDate { inner })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    /// Get today's Nepali date
    /// 
    /// Returns:
    ///     NepaliDate: Today's date in BS
    #[staticmethod]
    fn today() -> PyResult<Self> {
        npdatetime_core::NepaliDate::today()
            .map(|inner| NepaliDate { inner })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    /// Format the date as a string
    /// 
    /// Args:
    ///     format_str (str): Format string (strftime-style)
    /// 
    /// Returns:
    ///     str: Formatted date string
    /// 
    /// Example:
    ///     >>> date = NepaliDate(2077, 5, 19)
    ///     >>> date.format("%d %B %Y")
    ///     '19 Bhadra 2077'
    fn format(&self, format_str: &str) -> String {
        self.inner.format(format_str)
    }

    /// Add days to the date
    /// 
    /// Args:
    ///     days (int): Number of days to add (can be negative)
    /// 
    /// Returns:
    ///     NepaliDate: New date after adding days
    fn add_days(&self, days: i32) -> PyResult<Self> {
        self.inner.add_days(days)
            .map(|inner| NepaliDate { inner })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    /// Get the ordinal representation of the date (days since 1975-01-01 BS)
    fn to_ordinal(&self) -> i32 {
        self.inner.to_ordinal()
    }

    /// Create NepaliDate from an ordinal
    #[staticmethod]
    fn from_ordinal(ordinal: i32) -> PyResult<Self> {
        npdatetime_core::NepaliDate::from_ordinal(ordinal)
            .map(|inner| NepaliDate { inner })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    /// Get the Nepali Fiscal Year (e.g., "2080/81")
    #[getter]
    fn fiscal_year(&self) -> String {
        self.inner.fiscal_year()
    }

    /// Get the fiscal quarter (1-4)
    #[getter]
    fn fiscal_quarter(&self) -> u8 {
        self.inner.fiscal_quarter()
    }

    /// Format the date in Unicode Devanagari script
    fn format_unicode(&self) -> String {
        self.inner.format_unicode()
    }

    /// Generate a visual month calendar
    fn month_calendar(&self) -> String {
        self.inner.month_calendar()
    }

    /// Get the year
    #[getter]
    fn year(&self) -> i32 {
        self.inner.year
    }

    /// Get the month (1-12)
    #[getter]
    fn month(&self) -> u8 {
        self.inner.month
    }

    /// Get the day
    #[getter]
    fn day(&self) -> u8 {
        self.inner.day
    }

    /// String representation
    fn __str__(&self) -> String {
        format!("{}", self.inner)
    }

    /// Debug representation
    fn __repr__(&self) -> String {
        format!("NepaliDate({}, {}, {})", self.inner.year, self.inner.month, self.inner.day)
    }

    /// Equality comparison
    fn __eq__(&self, other: &Self) -> bool {
        self.inner == other.inner
    }

    /// Less than comparison
    fn __lt__(&self, other: &Self) -> bool {
        self.inner < other.inner
    }

    ///  Less than or equal comparison
    fn __le__(&self, other: &Self) -> bool {
        self.inner <= other.inner
    }

    /// Greater than comparison
    fn __gt__(&self, other: &Self) -> bool {
        self.inner > other.inner
    }

    /// Greater than or equal comparison
    fn __ge__(&self, other: &Self) -> bool {
        self.inner >= other.inner
    }
}

/// NPDateTime - Fast Nepali (Bikram Sambat) datetime library
#[pymodule]
fn npdatetime(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<NepaliDate>()?;
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}
