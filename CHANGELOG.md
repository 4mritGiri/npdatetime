# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-01-18

### Changed
- Promoted to stable 1.0.0 release for production use.
- Added "miti" to package keywords for better discovery.

### Added
- Comprehensive integration tests for public API verification.

## [0.1.0] - 2026-01-17

### Added
- Initial release of NPDateTime Rust library
- BS ↔ AD conversion (2000-2090 BS)
- Date formatting and parsing (strptime-like)
- Date arithmetic operations
- Nepali Fiscal Year logic and Quarter calculation
- Ordinal date support (to/from ordinal)
- Visual month calendar generator
- Python bindings via PyO3
- JavaScript/WASM bindings via wasm-bindgen
- Comprehensive test suite (69 tests, 100% passing)
- Benchmark suite showing <50ns lookup performance
- Professional documentation (User Guide, ROADMAP, etc.)

### Performance
- Lookup table access: 9-12 nanoseconds
- Date creation: 12 nanoseconds
- BS ↔ AD conversion: 6-8 microseconds
- Format operations: 98-640 nanoseconds

[Unreleased]: https://github.com/4mritGiri/npdatetime-rust/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/4mritGiri/npdatetime-rust/releases/tag/v0.1.0
