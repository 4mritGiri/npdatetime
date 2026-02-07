# NPDateTime Symfony Bundle

Symfony bundle for Nepali (Bikram Sambat) date handling, wrapping the `npdatetime` PHP extension.

## Requirements

- PHP 8.0 or higher
- Symfony 6.0+ or 7.0+
- npdatetime PHP extension installed

## Installation

### 1. Install the PHP Extension

First, install the `npdatetime` PHP extension. See [PHP bindings README](../php/README.md) for installation instructions.

### 2. Install the Bundle via Composer

```bash
composer require 4mritgiri/npdatetime-bundle
```

### 3. Enable the Bundle

If you're using Symfony Flex, the bundle will be registered automatically. Otherwise, register it manually in `config/bundles.php`:

```php
<?php

return [
    // ...
    Npdatetime\Bundle\NpdatetimeBundle::class => ['all' => true],
];
```

## Usage

### Inject the Service

The bundle provides `NepaliDateService` which you can inject into your services or controllers:

```php
<?php

namespace App\Controller;

use Npdatetime\Bundle\Service\NepaliDateService;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;

class DateController extends AbstractController
{
    public function __construct(
        private NepaliDateService $nepaliDateService
    ) {
    }

    public function index(): Response
    {
        // Get today's Nepali date
        $today = $this->nepaliDateService->today();
        
        // Create a specific Nepali date
        $date = $this->nepaliDateService->create(2077, 5, 19);
        
        // Convert from Gregorian
        $nepaliDate = $this->nepaliDateService->fromGregorian(2020, 9, 4);
        
        // Convert from DateTime
        $datetime = new \DateTime('2020-09-04');
        $nepaliDate = $this->nepaliDateService->fromDateTime($datetime);
        
        // Convert to DateTime
        $gregorianDate = $this->nepaliDateService->toDateTime($nepaliDate);
        
        // Format
        $formatted = $this->nepaliDateService->format($date, '%Y-%m-%d');
        
        return $this->json([
            'today' => (string) $today,
            'date' => (string) $date,
            'gregorian' => $gregorianDate->format('Y-m-d'),
            'formatted' => $formatted,
        ]);
    }
}
```

### Available Service Methods

#### `NepaliDateService`

- `create(int $year, int $month, int $day): NepaliDate` - Create a new Nepali date
- `fromGregorian(int $year, int $month, int $day): NepaliDate` - Create from Gregorian date
- `fromDateTime(\DateTimeInterface $dateTime): NepaliDate` - Create from PHP DateTime
- `today(): NepaliDate` - Get today's Nepali date
- `toDateTime(NepaliDate $nepaliDate): \DateTime` - Convert to PHP DateTime
- `format(NepaliDate $date, string $format = '%Y-%m-%d'): string` - Format the date

### Direct Extension Usage

You can also use the `NepaliDate` class directly:

```php
<?php

// Create a Nepali date
$date = new \NepaliDate(2077, 5, 19);

// Convert to Gregorian
[$year, $month, $day] = $date->to_gregorian();

// Create from Gregorian
$nepaliDate = \NepaliDate::from_gregorian(2020, 9, 4);

// Get today
$today = \NepaliDate::today();

// Format
echo $date->format('%Y-%m-%d');
```

## Format Strings

The extension supports the following format strings:

| Code | Description | Example |
|------|-------------|---------|
| `%Y` | 4-digit year | 2077 |
| `%m` | 2-digit month | 05 |
| `%d` | 2-digit day | 19 |
| `%B` | Full month name | Bhadra |
| `%b` | Short month name | Bha |

## Example: Date Converter Service

```php
<?php

namespace App\Service;

use Npdatetime\Bundle\Service\NepaliDateService;

class UserDateConverter
{
    public function __construct(
        private NepaliDateService $nepaliDateService
    ) {
    }

    public function convertUserBirthdate(\DateTime $gregorianBirthdate): array
    {
        $nepaliDate = $this->nepaliDateService->fromDateTime($gregorianBirthdate);
        
        return [
            'gregorian' => $gregorianBirthdate->format('Y-m-d'),
            'nepali' => $this->nepaliDateService->format($nepaliDate),
            'year' => $nepaliDate->get_year(),
            'month' => $nepaliDate->get_month(),
            'day' => $nepaliDate->get_day(),
        ];
    }
}
```

## License

MIT
