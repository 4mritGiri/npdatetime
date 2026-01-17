# Security Policy

## Supported Versions

Currently supporting:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in NPDateTime, please report it by:

1. **Email**: Send details to amritgiri.dev@gmail.com
2. **Include**: 
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will acknowledge your email within 48 hours and provide a detailed response within 7 days.

## Security Considerations

### Input Validation
- All date inputs are validated before processing
- Month values must be 1-12
- Day values are checked against calendar month lengths
- Year values must be within supported range (1975-2100 BS for lookup tables)

### Arithmetic Operations
- Date arithmetic operations check for overflows
- Conversion between calendars validates intermediate results

### Dependencies
- We minimize dependencies to reduce attack surface
- Dependencies are regularly audited and updated
- Optional features (astronomical, python, wasm) isolate complexity

## Best Practices

When using NPDateTime:
- Always handle `Result` types properly - don't unwrap blindly
- Validate user inputs before passing to library functions
- Use type system to enforce correctness
- Consider fuzzing your integration for edge cases

## Updates

Security updates will be released as patch versions and announced in CHANGELOG.md.
