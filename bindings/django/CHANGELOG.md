# Changelog

All notable changes to django-npdt will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.5] - 2025-07-XX

### Added
- **Dynamic Disabling Options**:
  - `disabled_dates` — disable specific dates (list of YYYY-MM-DD strings)
  - `disabled_days` — disable specific weekdays (list, range `"1-5"`, or mixed `"1-5,0"`)
  - `disable_past_dates` — disable all dates before today (future-only selection)
  - `disable_weekends` — disable weekends (Saturday in BS, Sunday in AD)
  - `disable_holidays` — disable holidays from the holiday provider
  - `on_date_disabled` — behavior when disabled date is selected (`'prevent'` or `'warn'`)
- **Holiday Provider System**:
  - `HolidayProvider` base class for custom holiday logic
  - `NepalPublicHolidays` built-in provider covering major Nepal public holidays (BS 2070–2100)
  - `CompositeHolidayProvider` to merge multiple providers
  - `StaticHolidayProvider` for quick one-off holiday lists
  - `HolidayDate` data class with `name`, `name_np`, and `type` fields
  - `show_holidays` option to highlight holidays visually (without disabling)
  - `holiday_provider` option for custom providers
  - `holidayNames` passed to JS picker for holiday tooltips
- **Django Admin Theme**:
  - `theme='admin'` option matching Django admin's color palette and font stack
  - `admin_theme=True` shortcut for `theme='admin'`
  - CSS isolation (`.npd-picker *` reset, `!important` overrides) to prevent admin CSS conflicts
- **Tithi on Hover**:
  - `show_tithi` option to display lunar tithi when hovering over a date
  - Tithi cached per month for performance
- **`widget_kwargs` on Form Fields**:
  - `NepaliDateField` and `NepaliDateRangeField` accept `widget_kwargs` to pass dynamic options through to the widget
- **Template Tag Enhancements**:
  - `{% nepali_date_picker %}` now supports `disable_past_dates`, `disable_weekends`, `disable_holidays`, `disabled_dates`, `disabled_days`, `show_tithi`, and `admin_theme`

### Fixed
- **WASM Memory Leaks**: All `NepaliDate` WASM objects are now properly freed after use. Fixed "memory access out of bounds" crashes in `renderDays()`, `selectDate()`, and other methods.
- **Django Admin CSS Conflicts**: Picker now uses CSS isolation (`isolation: isolate`, full descendant reset, `!important` overrides) to prevent host CSS from leaking in.
- **UI Overflow**: Fixed `npd-next` button overflowing the picker container with `overflow: hidden`, `min-width: 0`, and `flex-shrink` adjustments.

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
- Initial release of django-npdt
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

[Unreleased]: https://github.com/4mritGiri/npdatetime/compare/v0.2.5...HEAD
[0.2.5]: https://github.com/4mritGiri/npdatetime/compare/v0.1.6...v0.2.5
[0.1.6]: https://github.com/4mritGiri/npdatetime/compare/v0.1.0...v0.1.6
[0.1.0]: https://github.com/4mritGiri/npdatetime/releases/tag/v0.1.0
