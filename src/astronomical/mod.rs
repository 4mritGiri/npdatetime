//! Astronomical calculation approach (optional)
//!
//! Provides high-precision calculations for solar and lunar events.

pub mod calendar;
pub mod core;
pub mod lunar;
pub mod solar;

pub use calendar::BsCalendar as AstronomicalCalendar;
pub use lunar::tithi::TithiCalculator;
pub use solar::sankranti::SankrantiFinder;
