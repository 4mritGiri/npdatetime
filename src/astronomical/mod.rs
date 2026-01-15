//! Astronomical calculation approach (optional)
//! 
//! Provides high-precision calculations for solar and lunar events.

pub mod core;
pub mod solar;
pub mod lunar;
pub mod calendar;

pub use solar::sankranti::SankrantiFinder;
pub use lunar::tithi::TithiCalculator;
pub use calendar::BsCalendar as AstronomicalCalendar;
