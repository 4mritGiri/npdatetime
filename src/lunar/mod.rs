//! Lunar calculations module
//! 
//! Calculates Moon's position and Tithi

pub mod position;
pub mod tithi;
pub mod phases;

// pub use position::LunarCalculator;
// pub use tithi::{Tithi, calculate_tithi};
// pub use phases::MoonPhase;

/// Paksha (lunar fortnight)
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Paksha {
    Shukla,  // Waxing moon (1-15)
    Krishna, // Waning moon (16-30)
}

impl Paksha {
    pub fn from_tithi(tithi: u8) -> Self {
        if tithi <= 15 {
            Paksha::Shukla
        } else {
            Paksha::Krishna
        }
    }
}