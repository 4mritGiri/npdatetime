# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.5] - 2025-07-XX

### Added
- **Enterprise Date Picker Options** (JS + Django):
  - `disabledDates` / `disabled_dates` — disable specific dates
  - `disabledDays` / `disabled_days` — disable specific weekdays (supports list, range `"1-5"`, mixed `"1-5,0"`)
  - `disablePastDates` / `disable_past_dates` — disable all dates before today
  - `disableWeekends` / `disable_weekends` — disable weekends (Sat in BS, Sun in AD)
  - `disableHolidays` / `disable_holidays` — disable holidays from holiday provider
  - `holidayNames` — holiday name tooltips for dates
  - `onDateDisabled` / `on_date_disabled` — behavior when disabled date is selected (`'prevent'` or `'warn'`)
  - `showTithi` / `show_tithi` — show lunar tithi on date hover
- **Django Admin Theme**:
  - `theme='admin'` option matching Django admin's color palette (#417690, #ba2121) and font stack
  - `admin_theme=True` shortcut
  - CSS isolation (`.npd-picker *` reset, `!important` overrides, `isolation: isolate`) to prevent host CSS conflicts
- **Holiday Provider System** (Django):
  - `HolidayProvider` base class for custom holiday logic
  - `NepalPublicHolidays` built-in provider (major Nepal public holidays, BS 2070–2100)
  - `CompositeHolidayProvider` to merge multiple providers
  - `StaticHolidayProvider` for quick one-off holiday lists
  - `show_holidays` option to highlight holidays visually without disabling
- **`widget_kwargs` on Form Fields** (Django):
  - `NepaliDateField` and `NepaliDateRangeField` accept `widget_kwargs` to pass dynamic options through to the widget
- **Template Tag Enhancements** (Django):
  - `{% nepali_date_picker %}` now supports `disable_past_dates`, `disable_weekends`, `disable_holidays`, `disabled_dates`, `disabled_days`, `show_tithi`, and `admin_theme`
- **Publish Workflow** (Makefile):
  - `make publish` — tag current version and push to GitHub (triggers CI)
  - `make publish-dry` — dry run of publish
  - `make publish-bump VERSION=X.Y.Z` — bump version across all packages
  - `make publish-clean` — delete a version tag locally and remotely

### Fixed
- **WASM Memory Leaks**: All `NepaliDate` WASM objects now properly freed. Fixed "memory access out of bounds" crashes in `renderDays()`, `selectDate()`, and other hot paths. Added tithi/weekday caching to avoid repeated WASM allocations.
- **Django Admin CSS Conflicts**: Picker now uses CSS isolation to prevent host CSS from breaking the picker layout.
- **UI Overflow**: Fixed `npd-next` button overflowing the picker container.

## [0.1.6] - 2026-02-06

### Added
- **Fiscal Year Support**: Integrated fiscal year and quarter logic into Django model fields and template tags.
- **Dynamic Themes**: Added live theme synchronization for the date picker based on `html[data-theme]`.
- **Digit Translation**: Restored localized numeral support for the date picker UI.
- **Version Automation**: Improved CI/CD pipeline to automate version bumps and asset building across Rust, Python, WASM, and Django packages.

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

[Unreleased]: https://github.com/4mritGiri/npdatetime/compare/v0.2.5...HEAD
[0.2.5]: https://github.com/4mritGiri/npdatetime/compare/v0.1.6...v0.2.5
[0.1.6]: https://github.com/4mritGiri/npdatetime/compare/v0.1.0...v0.1.6
[0.1.0]: https://github.com/4mritGiri/npdatetime/releases/tag/v0.1.0
