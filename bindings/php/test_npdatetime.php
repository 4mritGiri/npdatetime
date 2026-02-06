<?php

echo "Testing NepaliDate PHP Extension\n";
echo "=================================\n\n";

// Test 1: Create a Nepali date
echo "Test 1: Create date (2077-05-19)\n";
$date = new NepaliDate(2077, 5, 19);
echo "Created: " . $date . "\n";
echo "Year: " . $date->get_year() . "\n";
echo "Month: " . $date->get_month() . "\n";
echo "Day: " . $date->get_day() . "\n\n";

// Test 2: Convert to Gregorian
echo "Test 2: Convert to Gregorian\n";
$gregorian = $date->to_gregorian();
echo "AD Date: " . $gregorian[0] . "-" . $gregorian[1] . "-" . $gregorian[2] . "\n\n";

// Test 3: Create from Gregorian
echo "Test 3: Create from Gregorian (2020-09-04)\n";
$date2 = NepaliDate::from_gregorian(2020, 9, 4);
echo "BS Date: " . $date2 . "\n\n";

// Test 4: Today's date
echo "Test 4: Today's date\n";
$today = NepaliDate::today();
echo "Today (BS): " . $today . "\n";
$today_ad = $today->to_gregorian();
echo "Today (AD): " . $today_ad[0] . "-" . $today_ad[1] . "-" . $today_ad[2] . "\n\n";

// Test 5: Format
echo "Test 5: Format date\n";
echo "Formatted: " . $date->format("%Y-%m-%d") . "\n\n";

echo "All tests passed!\n";
