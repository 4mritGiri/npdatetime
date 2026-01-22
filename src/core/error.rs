// Error types

use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub enum NpdatetimeError {
    InvalidDate(String),
    OutOfRange(String),
    ParseError(String),
    CalculationError(String),
}

impl fmt::Display for NpdatetimeError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            NpdatetimeError::InvalidDate(msg) => write!(f, "Invalid date: {}", msg),
            NpdatetimeError::OutOfRange(msg) => write!(f, "Out of range: {}", msg),
            NpdatetimeError::ParseError(msg) => write!(f, "Parse error: {}", msg),
            NpdatetimeError::CalculationError(msg) => write!(f, "Calculation error: {}", msg),
        }
    }
}

impl std::error::Error for NpdatetimeError {}

pub type Result<T> = std::result::Result<T, NpdatetimeError>;
