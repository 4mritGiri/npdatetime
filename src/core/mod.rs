//! Shared core types for the npdatetime library
//! 
//! Provides the primary date and datetime structures used across both
//! lookup-based and astronomical calculation methods.

pub mod date;
pub mod error;
// pub mod format; // Will enable once implemented

pub use date::NepaliDate;
pub use error::{NpdatetimeError, Result};