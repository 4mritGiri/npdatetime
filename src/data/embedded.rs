
// src/data/embedded.rs
include!(concat!(env!("OUT_DIR"), "/calendar_data.rs"));

pub fn get_days_in_month(year: i32, month: u8) -> Option<u8> {
    // Binary search or hash lookup in BS_CALENDAR_DATA
}