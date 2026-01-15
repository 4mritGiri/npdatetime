//! NPDateTime - High-performance Nepali (Bikram Sambat) datetime library
//! 
//! This library provides two approaches:
//! 1. **Lookup Tables** (default): Fast, accurate, works offline
//! 2. **Astronomical Calculations** (optional): Future-proof, educational

pub mod core;
#[cfg(feature = "lookup-tables")]
pub mod lookup;

#[cfg(feature = "astronomical")]
pub mod astronomical;

pub use core::date::NepaliDate;
pub use core::error::{NpdatetimeError, Result};

/// Prelude for common imports
pub mod prelude {
    pub use crate::core::date::NepaliDate;
    pub use crate::core::error::{NpdatetimeError, Result};
    
    #[cfg(feature = "astronomical")]
    pub use crate::astronomical::{SankrantiFinder, TithiCalculator, AstronomicalCalendar};
}

/// Library version
pub const VERSION: &str = env!("CARGO_PKG_VERSION");