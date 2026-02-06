# NPDateTime PHP Extension

PHP bindings for the `npdatetime` library, providing Nepali (Bikram Sambat) date conversion and manipulation in PHP.

## Requirements

- PHP 8.0 or higher with development headers
- Rust toolchain (1.70+)
- Cargo

## Installation

### From Source

1. **Install PHP development packages:**

```bash
# Ubuntu/Debian
sudo apt-get install php-dev

# macOS (via Homebrew)
brew install php

# Fedora/RHEL
sudo dnf install php-devel
```

2. **Build the extension:**

```bash
cd bindings/php
cargo build --release
```

3. **Install the extension:**

The compiled extension will be at `target/release/libnpdatetime_php.so` (Linux/Mac) or `target/release/npdatetime_php.dll` (Windows).

Copy it to your PHP extensions directory or load it directly:

```bash
# Find your extensions directory
php -i | grep extension_dir

# Copy the extension
sudo cp target/release/libnpdatetime_php.so /path/to/php/extensions/
```

4. **Enable the extension:**

Add to your `php.ini`:

```ini
extension=npdatetime_php
```

Or load dynamically in your script:

```php
<?php
dl('npdatetime_php.so');
```

## Usage

### Basic Example

```php
<?php

// Create a Nepali date
$date = new NepaliDate(2077, 5, 19);
echo $date; // Output: 2077-05-19

// Convert to Gregorian
$gregorian = $date->to_gregorian();
echo "{$gregorian[0]}-{$gregorian[1]}-{$gregorian[2]}"; // Output: 2020-9-4

// Create from Gregorian
$bs_date = NepaliDate::from_gregorian(2020, 9, 4);
echo $bs_date; // Output: 2077-05-19

// Get today's date
$today = NepaliDate::today();
echo $today;

// Format the date
echo $date->format("%Y-%m-%d"); // Output: 2077-05-19
```

### Available Methods

#### Constructor
- `new NepaliDate(int $year, int $month, int $day)` - Create a new Nepali date

#### Static Methods
- `NepaliDate::from_gregorian(int $year, int $month, int $day)` - Create from Gregorian date
- `NepaliDate::today()` - Get today's Nepali date

#### Instance Methods
- `to_gregorian()` - Convert to Gregorian, returns array `[year, month, day]`
- `format(string $format)` - Format the date
- `get_year()` - Get the year
- `get_month()` - Get the month (1-12)
- `get_day()` - Get the day

## Testing

Run the test script:

```bash
php -d extension=./target/release/libnpdatetime_php.so test_npdatetime.php
```

## License

MIT
