# Changelog

All notable changes to django-npdatetime will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.6] - 2026-02-06

### Added
- **Fiscal Year Support**:
  - New template filters: `fiscal_year` and `fiscal_quarter`.
  - Direct access to fiscal properties on model instances (e.g., `obj.date_field.fiscal_year`).
- **Dynamic Theme Synchronization**:
  - The date picker now automatically syncs with `html[data-theme]` when set to `auto`.
  - Added explicit light/dark theme overrides.
- **Improved Template Tags**:
  - Fixed `{% load nepali_date %}` by moving logic to a dedicated module.
  - Added new `{% nepali_date_picker %}` inclusion tag for inline usage.
  - Added missing `inline_picker.html` template.
- **Date Picker Refinements**:
  - Improved placeholders with format hints (e.g., "YYYY-MM-DD").
  - Restored localized numeral support in the UI while keeping standard input format.

## [0.1.0] - 2026-02-04

### Added
- Initial release of django-npdatetime
- Custom model fields:
  - `NepaliDateField` for storing Nepali dates
  - `NepaliDateTimeField` for storing Nepali dates with time
- Custom form fields:
  - `NepaliDateField` with validation
  - `NepaliDateTimeField` with validation
  - `NepaliDateRangeField` for date ranges
- Custom widgets:
  - `NepaliDatePickerWidget` with rich features
  - `NepaliDateRangeWidget` for selecting date ranges
- Template tags and filters:
  - `to_nepali_date` - Convert Gregorian to Nepali
  - `to_gregorian_date` - Convert Nepali to Gregorian
  - `format_nepali_date` - Format Nepali dates
  - `nepali_month_name` - Get month names
  - `to_nepali_number` - Convert to Nepali numerals
  - `nepali_date_today` - Get today's Nepali date
- Utility functions for date conversion and validation
- Django admin integration
- Bilingual support (English and Nepali)
- Multiple theme support (auto, light, dark)
- Comprehensive documentation and examples

[Unreleased]: https://github.com/4mritGiri/npdatetime-rust/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/4mritGiri/npdatetime-rust/releases/tag/v0.1.0
