# Project Roadmap
## NPDateTime - Development Plan

---

## 🎯 Phase 1: Core Library (Weeks 1-4)

### ✅ Code Quality

#### 1.1 Complete Implementation
- [ ] **Lookup table fully working** (2000-2090 BS)
  - [ ] All 12 months × 91 years validated
  - [ ] BS ↔ AD conversion 100% accurate
  - [ ] Edge cases handled (year boundaries)
  
- [ ] **Astronomical calculator** (optional feature)
  - [ ] Solar position calculations
  - [ ] Sankranti finder
  - [ ] Month length calculator
  - [ ] Validated against lookup table

- [ ] **Core date operations**
  - [ ] Date creation and validation
  - [ ] Date arithmetic (add/subtract days)
  - [ ] Date comparison
  - [ ] Formatting (strftime-like)
  - [ ] Parsing (strptime-like)

#### 1.2 Error Handling
```rust
// NO unwrap() in library code (only in tests/examples)
❌ let date = parse_date(input).unwrap();
✅ let date = parse_date(input)?;

// Descriptive error messages
❌ Err("invalid")
✅ Err(NpDateTimeError::InvalidDate {
    year: 2077,
    month: 13,
    message: "Month must be between 1 and 12"
})
```

#### 1.3 API Design

**Checklist:**
- [ ] API is intuitive and follows Rust conventions
- [ ] Method names are clear and consistent
- [ ] No breaking changes needed after 1.0
- [ ] Follows semver (semantic versioning)

**Example of good API:**
```rust
// Simple and intuitive
let date = NepaliDate::from_ymd(2077, 5, 19)?;
let gregorian = date.to_gregorian();
let formatted = date.format("%Y-%m-%d");

// Chainable operations
let future = NepaliDate::today()?
    .add_days(30)
    .add_months(2);
```

---

## 📚 Phase 2: Documentation (Weeks 5-6)

### ✅ README.md - First Impression

Your README must have:

```markdown
# NPDateTime 🇳🇵

[![Crates.io](https://img.shields.io/crates/v/npdatetime.svg)](https://crates.io/crates/npdatetime)
[![Documentation](https://docs.rs/npdatetime/badge.svg)](https://docs.rs/npdatetime)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Build Status](https://github.com/yourusername/npdatetime/workflows/CI/badge.svg)](https://github.com/yourusername/npdatetime/actions)

Fast and accurate Nepali (Bikram Sambat) date and time library for Rust.

## ✨ Features

- 🚀 **Blazing Fast** - 100x faster than Python alternatives
- 🎯 **100% Accurate** - Verified against official BS calendar data
- 🌍 **Multi-platform** - Rust, Python, JavaScript, Java bindings
- 📅 **Complete BS Calendar** - Supports years 2000-2090 BS
- 🔍 **Astronomical Calculator** - Optional high-precision mode
- ⚡ **Zero Dependencies** - Core library has no dependencies

## 🚀 Quick Start

### Rust
\```rust
use npdatetime::NepaliDate;

// Create date
let date = NepaliDate::from_ymd(2077, 5, 19)?;

// Convert to Gregorian
let gregorian = date.to_gregorian(); // (2020, 9, 4)

// Format
println!("{}", date.format("%d %B %Y")); // "19 Bhadra 2077"
\```

### Python
\```python
from npdatetime import NepaliDate

date = NepaliDate(2077, 5, 19)
print(date.to_gregorian())  # datetime.date(2020, 9, 4)
\```

## 📦 Installation

### Rust
\```toml
[dependencies]
npdatetime = "1.0"
\```

### Python
\```bash
pip install npdatetime
\```

### JavaScript
\```bash
npm install npdatetime
\```

## 📖 Documentation

- [API Documentation](https://docs.rs/npdatetime)
- [User Guide](https://npdatetime.readthedocs.io)
- [Examples](./examples)
- [Changelog](./CHANGELOG.md)

## 🎯 Use Cases

- Web applications with Nepali calendar support
- Data analysis with Nepali dates
- Government and business applications in Nepal
- Historical date conversions
- Festival and event calculators

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Acknowledgments

- Based on official Nepal calendar data
- Astronomical algorithms from Jean Meeus
- Inspired by [your Python library](https://github.com/4mritGiri/npdatetime)
```

### ✅ API Documentation

**Every public item needs docs:**

```rust
/// Represents a date in the Bikram Sambat calendar.
///
/// The Bikram Sambat (BS) calendar is the official calendar of Nepal.
/// This type provides methods for creating, manipulating, and formatting
/// BS dates.
///
/// # Examples
///
/// ```
/// use npdatetime::NepaliDate;
///
/// // Create a date
/// let date = NepaliDate::from_ymd(2077, 5, 19)?;
///
/// // Convert to Gregorian
/// let (year, month, day) = date.to_gregorian();
/// assert_eq!((year, month, day), (2020, 9, 4));
///
/// // Format the date
/// assert_eq!(date.format("%Y-%m-%d"), "2077-05-19");
/// # Ok::<(), npdatetime::Error>(())
/// ```
///
/// # Date Range
///
/// Supported range: 2000/01/01 BS to 2090/12/30 BS
pub struct NepaliDate {
    // ...
}
```

**Checklist:**
- [ ] All public functions documented
- [ ] Code examples in documentation
- [ ] Examples compile and run (`cargo test --doc`)
- [ ] Module-level documentation explaining purpose

### ✅ User Guide

Create `docs/guide.md`:

```markdown
# NPDateTime User Guide

## Table of Contents
1. Installation
2. Basic Usage
3. Date Operations
4. Formatting and Parsing
5. Timezone Support
6. Performance Tips
7. Migration from Other Libraries
8. FAQ

## 1. Installation
...

## 2. Basic Usage

### Creating Dates
...

### Converting Dates
...
```

### ✅ Examples

Create comprehensive examples in `examples/`:

- [ ] `examples/basic_usage.rs` - Simple date operations
- [ ] `examples/conversion_demo.rs` - BS ↔ AD conversion
- [ ] `examples/formatting.rs` - All format options
- [ ] `examples/date_arithmetic.rs` - Add/subtract operations
- [ ] `examples/real_world_app.rs` - Complete mini-app
- [ ] `examples/performance_comparison.rs` - Benchmarks

---

## 🧪 Phase 3: Testing (Weeks 7-8)

### ✅ Test Coverage

**Target: >80% code coverage**

```bash
# Install tarpaulin
cargo install cargo-tarpaulin

# Run coverage
cargo tarpaulin --out Html --output-dir coverage
```

**Test pyramid:**

```
         /\
        /  \  Unit Tests (70%)
       /────\
      /      \  Integration Tests (20%)
     /────────\
    /          \  E2E Tests (10%)
   /────────────\
```

### ✅ Test Types

#### Unit Tests
```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_valid_date_creation() {
        let date = NepaliDate::from_ymd(2077, 5, 19).unwrap();
        assert_eq!(date.year(), 2077);
        assert_eq!(date.month(), 5);
        assert_eq!(date.day(), 19);
    }
    
    #[test]
    fn test_invalid_month() {
        let result = NepaliDate::from_ymd(2077, 13, 1);
        assert!(result.is_err());
    }
    
    #[test]
    fn test_invalid_day() {
        // Month 5 of 2077 has 31 days
        assert!(NepaliDate::from_ymd(2077, 5, 32).is_err());
    }
}
```

#### Integration Tests

Create `tests/integration_test.rs`:

```rust
use npdatetime::NepaliDate;

#[test]
fn test_round_trip_conversion() {
    // BS → AD → BS should give same date
    let original = NepaliDate::from_ymd(2077, 5, 19).unwrap();
    let gregorian = original.to_gregorian();
    let back = NepaliDate::from_gregorian(
        gregorian.0, 
        gregorian.1, 
        gregorian.2
    ).unwrap();
    
    assert_eq!(original, back);
}

#[test]
fn test_all_months_all_years() {
    // Validate entire supported range
    for year in 2000..=2090 {
        for month in 1..=12 {
            let days = NepaliDate::days_in_month(year, month).unwrap();
            assert!(days >= 29 && days <= 32);
            
            // First and last day of month should be valid
            assert!(NepaliDate::from_ymd(year, month, 1).is_ok());
            assert!(NepaliDate::from_ymd(year, month, days).is_ok());
            assert!(NepaliDate::from_ymd(year, month, days + 1).is_err());
        }
    }
}
```

#### Property-Based Testing

Add `proptest`:

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_date_arithmetic_commutative(days in 1..365i32) {
        let date = NepaliDate::from_ymd(2077, 1, 1).unwrap();
        let forward_then_back = date.add_days(days).add_days(-days);
        let back_then_forward = date.add_days(-days).add_days(days);
        prop_assert_eq!(forward_then_back, back_then_forward);
    }
}
```

**Test Checklist:**
- [ ] All public APIs tested
- [ ] Edge cases covered
- [ ] Error cases tested
- [ ] Integration tests for workflows
- [ ] Property-based tests for invariants
- [ ] Fuzz testing for parser

---

## 🔧 Phase 4: CI/CD (Week 9)

### ✅ GitHub Actions

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    name: Test
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        rust: [stable, beta, nightly]
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions-rs/toolchain@v1
        with:
          toolchain: ${{ matrix.rust }}
          override: true
      
      - name: Run tests
        run: cargo test --all-features
      
      - name: Run doc tests
        run: cargo test --doc

  clippy:
    name: Clippy
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions-rs/toolchain@v1
        with:
          toolchain: stable
          components: clippy
          override: true
      - run: cargo clippy --all-targets --all-features -- -D warnings

  fmt:
    name: Rustfmt
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions-rs/toolchain@v1
        with:
          toolchain: stable
          components: rustfmt
          override: true
      - run: cargo fmt --all -- --check

  coverage:
    name: Coverage
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions-rs/toolchain@v1
        with:
          toolchain: stable
          override: true
      - uses: actions-rs/tarpaulin@v0.1
        with:
          args: '--all-features --workspace --timeout 600 --out Xml'
      - uses: codecov/codecov-action@v3

  security:
    name: Security Audit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions-rs/audit-check@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
```

### ✅ Pre-commit Hooks

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: cargo-fmt
        name: cargo fmt
        entry: cargo fmt --all -- --check
        language: system
        pass_filenames: false
        
      - id: cargo-clippy
        name: cargo clippy
        entry: cargo clippy --all-targets --all-features -- -D warnings
        language: system
        pass_filenames: false
        
      - id: cargo-test
        name: cargo test
        entry: cargo test --all-features
        language: system
        pass_filenames: false
```

---

## 📦 Phase 5: Publishing (Week 10)

### ✅ Crates.io Preparation

#### 5.1 Update `Cargo.toml`

```toml
[package]
name = "npdatetime"
version = "1.0.0"
edition = "2021"
authors = ["Your Name <your.email@example.com>"]
description = "Fast and accurate Nepali (Bikram Sambat) date and time library"
documentation = "https://docs.rs/npdatetime"
homepage = "https://github.com/yourusername/npdatetime"
repository = "https://github.com/yourusername/npdatetime"
readme = "README.md"
license = "MIT"
keywords = ["nepali", "bikram-sambat", "calendar", "datetime", "nepal"]
categories = ["date-and-time", "localization", "internationalization"]
exclude = [
    "/.github",
    "/target",
    "/benches",
    "*.png",
]

[package.metadata.docs.rs]
all-features = true
rustdoc-args = ["--cfg", "docsrs"]
```

#### 5.2 Versioning Strategy

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.x.x): Breaking API changes
- **MINOR** (x.1.x): New features, backward compatible
- **PATCH** (x.x.1): Bug fixes

#### 5.3 CHANGELOG.md

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-01-20

### Added
- Initial release
- BS to AD conversion (2000-2090 BS)
- Date formatting and parsing
- Date arithmetic operations
- Astronomical calculator (optional)

### Performance
- 100x faster than Python alternatives
- Zero-copy operations where possible
```

#### 5.4 Publish Checklist

- [ ] `cargo package` succeeds without warnings
- [ ] All tests pass on CI
- [ ] Documentation builds without errors
- [ ] CHANGELOG.md updated
- [ ] Version bumped in Cargo.toml
- [ ] Git tag created (`git tag v1.0.0`)
- [ ] Run `cargo publish --dry-run`
- [ ] Run `cargo publish`

---

## 🌍 Phase 6: Multi-Language Bindings (Weeks 11-14)

### ✅ Python Bindings (PyPI)

**Setup in `bindings/python/`:**

```python
# pyproject.toml
[build-system]
requires = ["maturin>=1.0,<2.0"]
build-backend = "maturin"

[project]
name = "npdatetime"
version = "1.0.0"
description = "Fast Nepali datetime library (Rust bindings)"
requires-python = ">=3.7"
classifiers = [
    "Programming Language :: Rust",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
]

# src/lib.rs (Python bindings)
use pyo3::prelude::*;

#[pyclass]
struct NepaliDate {
    inner: npdatetime::NepaliDate,
}

#[pymethods]
impl NepaliDate {
    #[new]
    fn new(year: i32, month: u8, day: u8) -> PyResult<Self> {
        Ok(NepaliDate {
            inner: npdatetime::NepaliDate::from_ymd(year, month, day)
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(
                    e.to_string()
                ))?,
        })
    }
    
    fn to_gregorian(&self) -> (i32, u8, u8) {
        self.inner.to_gregorian()
    }
}

#[pymodule]
fn npdatetime(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<NepaliDate>()?;
    Ok(())
}
```

**Publish:**
```bash
cd bindings/python
maturin build --release
maturin publish
```

### ✅ JavaScript/WASM (npm)

```bash
cd bindings/javascript
wasm-pack build --target web --release
wasm-pack publish
```

### ✅ Java Bindings (Maven Central)

Use JNI - more complex, consider if there's demand.

---

## 🎨 Phase 7: Marketing & Community (Weeks 15-16)

### ✅ Create Website

**Options:**
1. GitHub Pages (free)
2. Netlify (free)
3. Vercel (free)

**Content:**
```
npdatetime.org/
├── index.html          # Landing page
├── docs/               # Documentation
├── examples/           # Interactive examples
├── playground/         # Try it online (WASM)
└── blog/               # Release announcements
```

### ✅ Write Launch Blog Post

**Title:** "Introducing NPDateTime: Lightning-Fast Nepali Date Library"

**Sections:**
1. Problem: Existing solutions are slow/inaccurate
2. Solution: NPDateTime with Rust performance
3. Features: What makes it special
4. Benchmarks: Show 100x speedup
5. Getting Started: Quick examples
6. Roadmap: Future plans

**Publish on:**
- Dev.to
- Medium
- Hacker News
- Reddit (r/rust, r/Nepal)
- Twitter/X

### ✅ Community Building

**Communication Channels:**
- [ ] GitHub Discussions enabled
- [ ] Discord server (optional)
- [ ] Twitter/X account
- [ ] Stack Overflow tag monitoring

**Engagement:**
- [ ] Respond to issues within 24 hours
- [ ] Welcome first-time contributors
- [ ] Monthly project updates
- [ ] Highlight community contributions

---

## 📊 Phase 8: Monitoring & Maintenance (Ongoing)

### ✅ Metrics to Track

**Download Stats:**
- crates.io downloads
- PyPI downloads
- npm downloads

**Quality Metrics:**
- Test coverage (>80%)
- Documentation coverage (100%)
- Open issues vs closed
- PR response time

**Community Health:**
- GitHub stars
- Contributors
- Forks
- Dependencies (dependents)

### ✅ Dependency Management

```bash
# Check for outdated dependencies
cargo outdated

# Security audit
cargo audit

# Update dependencies (carefully!)
cargo update
```

### ✅ Release Process

**Every release:**
1. Update CHANGELOG.md
2. Bump version in Cargo.toml
3. Run full test suite
4. Update documentation
5. Create git tag
6. Publish to crates.io
7. Publish bindings (Python, JS)
8. Create GitHub release
9. Announce on social media

---

## ✅ Production-Grade Checklist Summary

### Must-Have (MVP)
- [ ] Core functionality complete and tested
- [ ] Zero `unwrap()` in library code
- [ ] Good README with examples
- [ ] API documentation
- [ ] CI/CD pipeline
- [ ] Published to crates.io
- [ ] MIT License
- [ ] CHANGELOG.md

### Should-Have (v1.0)
- [ ] >80% test coverage
- [ ] Multi-platform CI (Linux, Mac, Windows)
- [ ] User guide
- [ ] Python bindings
- [ ] Security audit passes
- [ ] Clippy/fmt in CI
- [ ] Comprehensive examples

### Nice-to-Have (v1.x)
- [ ] JavaScript/WASM bindings
- [ ] Website with playground
- [ ] Blog posts
- [ ] Community Discord
- [ ] >1000 GitHub stars
- [ ] Listed on awesome-rust
- [ ] Conference talk

---

## 🚀 Quick Start Timeline

**Month 1:** Code quality + docs
**Month 2:** Testing + CI/CD
**Month 3:** Publishing + bindings
**Month 4:** Marketing + community

**By Month 4, you should have:**
- Production-grade Rust library
- Python and JavaScript bindings
- 80%+ test coverage
- Professional documentation
- Active community

---

## 📞 Need Help?

**Resources:**
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [The Cargo Book](https://doc.rust-lang.org/cargo/)
- [docs.rs Publishing Guide](https://docs.rs/about)
- [PyO3 User Guide](https://pyo3.rs/)
- [wasm-pack Documentation](https://rustwasm.github.io/wasm-pack/)

**Communities:**
- [Rust Users Forum](https://users.rust-lang.org/)
- [r/rust](https://reddit.com/r/rust)
- [Rust Discord](https://discord.gg/rust-lang)

---

## 🎯 Success Metrics

**After 6 months:**
- 10,000+ downloads
- 100+ GitHub stars
- 10+ contributors
- Used in 5+ production apps
- Featured in Rust newsletter

**After 1 year:**
- 100,000+ downloads
- 500+ stars
- De-facto standard for Nepali dates
- Multiple language bindings
- Active community

Good luck building the best Nepali datetime library! 🚀🇳🇵