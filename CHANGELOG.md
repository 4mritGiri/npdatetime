# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-01-17

### Added
- Initial release of NPDateTime Rust library
- Core `NepaliDate` type with BS ↔ AD conversions
- Fast lookup-table based date conversions (1975-2100 BS)
- Astronomical calculation module with VSOP87 and ELP-2000
- Solar Sankranti (zodiac transit) finder with ±10 second accuracy
- Lunar Tithi calculator supporting all 30 tithis
- Leap month (Adhika Masa) detection
- Format module with strftime-style patterns
- Unicode Devanagari number support
- Date arithmetic (`add_days`)
- Python bindings via PyO3
- JavaScript/WASM bindings via wasm-bindgen
- Comprehensive test suite (67 tests, 100% passing)
- Benchmark suite showing <50ns lookup performance
- Complete documentation

### Performance
- Lookup table access: 9-12 nanoseconds
- Date creation: 12 nanoseconds
- BS ↔ AD conversion: 6-8 microseconds
- Format operations: 98-640 nanoseconds

[Unreleased]: https://github.com/4mritGiri/npdatetime-rust/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/4mritGiri/npdatetime-rust/releases/tag/v0.1.0
