//! # NPDateTime
//!
//! High-performance Nepali (Bikram Sambat) datetime library featuring both
//! lightning-fast lookup-based conversions and high-precision astronomical calculations.
//!
//! ## Key Features
//! - **Hybrid Approach**: Use embedded lookup tables for instant results or full astronomical theories (VSOP87, ELP-2000) for future-proof accuracy.
//! - **Modular Design**: Easily swap between fast civil calendar logic and precise astronomical events.
//! - **Cross-Language**: Architected for bindings in Python, JavaScript, Java, and PHP.
//! - **Performance**: Core logic is written in Rust for maximum speed and memory safety.
//! - **No-std Support**: Core components are designed to run on embedded systems.
//!
//! ## Feature Flags
//! - `lookup-tables` (default): Enables CSV-backed pre-calculated calendar data (1975-2100 BS).
//! - `astronomical`: Enables full solar and lunar position calculations for any date range.
//! - `std`: Enables standard library features including `Chrono` integration.
//! - `wasm`: Enables WASM bindings for web usage.
//!

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
    pub use crate::astronomical::{AstronomicalCalendar, SankrantiFinder, TithiCalculator};
}

/// Library version
pub const VERSION: &str = env!("CARGO_PKG_VERSION");
