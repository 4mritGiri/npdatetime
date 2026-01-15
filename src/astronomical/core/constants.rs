//! Astronomical and mathematical constants

use core::f64::consts::PI;

/// Degrees to radians conversion factor
pub const DEG_TO_RAD: f64 = PI / 180.0;

/// Radians to degrees conversion factor
pub const RAD_TO_DEG: f64 = 180.0 / PI;

/// Arcseconds to radians
pub const ARCSEC_TO_RAD: f64 = PI / (180.0 * 3600.0);

/// Julian Day of J2000.0 epoch (January 1, 2000, 12:00 TT)
pub const J2000_0: f64 = 2451545.0;

/// Days per Julian century
pub const DAYS_PER_CENTURY: f64 = 36525.0;

/// Astronomical Unit in kilometers
pub const AU_KM: f64 = 149597870.7;

/// Speed of light in km/s
pub const SPEED_OF_LIGHT: f64 = 299792.458;

/// Synodic month (average lunar month in days)
pub const SYNODIC_MONTH: f64 = 29.530588853;

/// Tropical year (solar year in days)
pub const TROPICAL_YEAR: f64 = 365.242189;

/// Sidereal month
pub const SIDEREAL_MONTH: f64 = 27.321661;

/// Earth's obliquity at J2000.0 (in degrees)
pub const OBLIQUITY_J2000: f64 = 23.4392911;

/// Zodiac signs (30 degrees each)
pub const ZODIAC_DEGREES: f64 = 30.0;

/// Number of zodiac signs
pub const NUM_ZODIAC_SIGNS: u8 = 12;

/// Degrees in full circle
pub const FULL_CIRCLE: f64 = 360.0;

/// Tithi duration in degrees (Moon advances 12° relative to Sun)
pub const TITHI_DEGREES: f64 = 12.0;

/// Number of Tithis per lunar month
pub const NUM_TITHIS: u8 = 30;

/// Nepal timezone offset from UTC (in hours)
pub const NEPAL_TZ_OFFSET: f64 = 5.75; // UTC+5:45

/// Nepal latitude (Kathmandu)
pub const NEPAL_LATITUDE: f64 = 27.7172;

/// Nepal longitude (Kathmandu)
pub const NEPAL_LONGITUDE: f64 = 85.3240;
