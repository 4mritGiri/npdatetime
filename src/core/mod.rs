//! Core utilities for astronomical calculations
//! 
//! Handles time conversion, constants, and root finding

pub mod constants;
pub mod time;
pub mod newton_raphson;

pub use time::JulianDay;
pub use newton_raphson::NewtonRaphsonSolver;

/// Zodiac signs
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ZodiacSign {
    Aries = 0,      // Mesh (बैशाख)
    Taurus = 1,     // Vrishabha (जेष्ठ)
    Gemini = 2,     // Mithuna (आषाढ)
    Cancer = 3,     // Karka (श्रावण)
    Leo = 4,        // Simha (भाद्र)
    Virgo = 5,      // Kanya (आश्विन)
    Libra = 6,      // Tula (कार्तिक)
    Scorpio = 7,    // Vrishchika (मंसिर)
    Sagittarius = 8,// Dhanu (पौष)
    Capricorn = 9,  // Makara (माघ)
    Aquarius = 10,  // Kumbha (फाल्गुन)
    Pisces = 11,    // Meena (चैत्र)
}

impl ZodiacSign {
    /// Get longitude where this sign starts (in degrees)
    pub fn start_longitude(&self) -> f64 {
        (*self as u8 as f64) * 30.0
    }

    /// Get BS month corresponding to this zodiac sign
    pub fn to_bs_month(&self) -> u8 {
        (*self as u8 + 1) % 12 + 1
    }
}