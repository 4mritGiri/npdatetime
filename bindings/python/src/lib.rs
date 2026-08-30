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

    /// Get Tithi for the date (Astronomical calculation)
    /// 
    /// Returns:
    ///     str: Tithi name (e.g., "Shukla Pratipada", "Krishna Dwitiya", "Purnima", "Amavasya")
    fn tithi(&self) -> PyResult<String> {
        let (y, m, d) = self.inner.to_gregorian()
            .map_err(|e| PyValueError::new_err(e.to_string()))?;

        use npdatetime_core::astronomical::core::JulianDay;
        use npdatetime_core::astronomical::TithiCalculator;

        let jd = JulianDay::from_gregorian(y, m as u8, d as u8, 12.0);
        let tithi = TithiCalculator::get_tithi(jd);

        Ok(format!("{} {}", tithi.paksha, tithi.name()))
    }

    /// Get detailed Tithi information including start and end times in Nepal Standard Time (NPT)
    /// 
    /// Returns:
    ///     dict: { "name": str, "paksha": str, "index": int, "start_time": str, "end_time": str }
    fn tithi_details(&self, py: Python) -> PyResult<PyObject> {
        let (y, m, d) = self.inner.to_gregorian()
            .map_err(|e| PyValueError::new_err(e.to_string()))?;

        use npdatetime_core::astronomical::core::constants::NEPAL_TZ_OFFSET;
        use npdatetime_core::astronomical::core::JulianDay;
        use npdatetime_core::astronomical::TithiCalculator;

        let jd_mid = JulianDay::from_gregorian(y, m as u8, d as u8, 12.0);
        let tithi = TithiCalculator::get_tithi(jd_mid);

        let start_jd = TithiCalculator::find_tithi_end(tithi.index - 1, jd_mid)
            .unwrap_or(jd_mid);
        let end_jd = TithiCalculator::find_tithi_end(tithi.index, jd_mid)
            .unwrap_or(jd_mid);

        let start_npt = start_jd.add_days(NEPAL_TZ_OFFSET / 24.0);
        let end_npt = end_jd.add_days(NEPAL_TZ_OFFSET / 24.0);

        let (sy, sm, sd, shour) = start_npt.to_gregorian();
        let (ey, em, ed, ehour) = end_npt.to_gregorian();

        fn format_time(y: i32, m: u8, d: u8, hour_float: f64) -> String {
            let total_secs = (hour_float * 3600.0).round() as u32;
            let h = (total_secs / 3600) % 24;
            let min = (total_secs % 3600) / 60;
            let sec = total_secs % 60;
            format!("{:04}-{:02}-{:02} {:02}:{:02}:{:02}", y, m, d, h, min, sec)
        }

        let dict = pyo3::types::PyDict::new_bound(py);
        dict.set_item("name", format!("{} {}", tithi.paksha, tithi.name()))?;
        dict.set_item("paksha", format!("{}", tithi.paksha))?;
        dict.set_item("index", tithi.index)?;
        dict.set_item("start_time", format_time(sy, sm, sd, shour))?;
        dict.set_item("end_time", format_time(ey, em, ed, ehour))?;

        Ok(dict.into())
    }
}

/// Astronomical Bikram Sambat date representation
#[pyclass]
#[derive(Clone)]
struct BsDate {
    inner: npdatetime_core::astronomical::BsDate,
}

#[pymethods]
impl BsDate {
    /// Create a new astronomical BS date
    #[new]
    fn new(year: i32, month: u8, day: u8) -> PyResult<Self> {
        npdatetime_core::astronomical::BsDate::new(year, month, day)
            .map(|inner| BsDate { inner })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    /// Create BsDate from Gregorian (AD) date
    #[staticmethod]
    fn from_gregorian(year: i32, month: u8, day: u8) -> PyResult<Self> {
        npdatetime_core::astronomical::BsDate::from_gregorian(year, month, day)
            .map(|inner| BsDate { inner })
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    /// Convert to Gregorian (AD) date
    fn to_gregorian(&self) -> PyResult<(i32, u8, u8)> {
        self.inner.to_gregorian()
            .map(|(y, m, d)| (y, m as u8, d as u8))
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    /// Get the year
    #[getter]
    fn year(&self) -> i32 {
        self.inner.year
    }

    /// Get the month
    #[getter]
    fn month(&self) -> u8 {
        self.inner.month
    }

    /// Get the day
    #[getter]
    fn day(&self) -> u8 {
        self.inner.day
    }

    /// Get Tithi for the date (Astronomical)
    fn tithi(&self) -> PyResult<String> {
        let (y, m, d) = self.inner.to_gregorian()
            .map_err(|e| PyValueError::new_err(e.to_string()))?;

        use npdatetime_core::astronomical::core::JulianDay;
        use npdatetime_core::astronomical::TithiCalculator;

        let jd = JulianDay::from_gregorian(y, m as u8, d as u8, 12.0);
        let tithi = TithiCalculator::get_tithi(jd);

        Ok(format!("{} {}", tithi.paksha, tithi.name()))
    }

    /// Get detailed Tithi information including start and end times in Nepal Standard Time (NPT)
    fn tithi_details(&self, py: Python) -> PyResult<PyObject> {
        let (y, m, d) = self.inner.to_gregorian()
            .map_err(|e| PyValueError::new_err(e.to_string()))?;

        use npdatetime_core::astronomical::core::constants::NEPAL_TZ_OFFSET;
        use npdatetime_core::astronomical::core::JulianDay;
        use npdatetime_core::astronomical::TithiCalculator;

        let jd_mid = JulianDay::from_gregorian(y, m as u8, d as u8, 12.0);
        let tithi = TithiCalculator::get_tithi(jd_mid);

        let start_jd = TithiCalculator::find_tithi_end(tithi.index - 1, jd_mid)
            .unwrap_or(jd_mid);
        let end_jd = TithiCalculator::find_tithi_end(tithi.index, jd_mid)
            .unwrap_or(jd_mid);

        let start_npt = start_jd.add_days(NEPAL_TZ_OFFSET / 24.0);
        let end_npt = end_jd.add_days(NEPAL_TZ_OFFSET / 24.0);

        let (sy, sm, sd, shour) = start_npt.to_gregorian();
        let (ey, em, ed, ehour) = end_npt.to_gregorian();

        fn format_time(y: i32, m: u8, d: u8, hour_float: f64) -> String {
            let total_secs = (hour_float * 3600.0).round() as u32;
            let h = (total_secs / 3600) % 24;
            let min = (total_secs % 3600) / 60;
            let sec = total_secs % 60;
            format!("{:04}-{:02}-{:02} {:02}:{:02}:{:02}", y, m, d, h, min, sec)
        }

        let dict = pyo3::types::PyDict::new_bound(py);
        dict.set_item("name", format!("{} {}", tithi.paksha, tithi.name()))?;
        dict.set_item("paksha", format!("{}", tithi.paksha))?;
        dict.set_item("index", tithi.index)?;
        dict.set_item("start_time", format_time(sy, sm, sd, shour))?;
        dict.set_item("end_time", format_time(ey, em, ed, ehour))?;

        Ok(dict.into())
    }

    fn __str__(&self) -> String {
        format!("{}", self.inner)
    }

    fn __repr__(&self) -> String {
        format!("BsDate({}, {}, {})", self.inner.year, self.inner.month, self.inner.day)
    }
}

/// NPDateTime - Fast Nepali (Bikram Sambat) datetime library
#[pymodule]
fn npdatetime(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<NepaliDate>()?;
    m.add_class::<BsDate>()?;
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("__all__", vec!["NepaliDate", "BsDate", "__version__"])?;
    Ok(())
}
