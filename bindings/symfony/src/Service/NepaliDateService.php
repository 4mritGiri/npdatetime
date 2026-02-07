<?php

namespace Npdatetime\Bundle\Service;

/**
 * Service wrapper for NepaliDate PHP extension
 */
class NepaliDateService
{
    /**
     * Create a new Nepali date
     */
    public function create(int $year, int $month, int $day): \NepaliDate
    {
        return new \NepaliDate($year, $month, $day);
    }

    /**
     * Create NepaliDate from Gregorian date
     */
    public function fromGregorian(int $year, int $month, int $day): \NepaliDate
    {
        return \NepaliDate::from_gregorian($year, $month, $day);
    }

    /**
     * Create NepaliDate from DateTime
     */
    public function fromDateTime(\DateTimeInterface $dateTime): \NepaliDate
    {
        return \NepaliDate::from_gregorian(
            (int) $dateTime->format('Y'),
            (int) $dateTime->format('m'),
            (int) $dateTime->format('d')
        );
    }

    /**
     * Get today's Nepali date
     */
    public function today(): \NepaliDate
    {
        return \NepaliDate::today();
    }

    /**
     * Convert NepaliDate to DateTime
     */
    public function toDateTime(\NepaliDate $nepaliDate): \DateTime
    {
        [$year, $month, $day] = $nepaliDate->to_gregorian();
        return new \DateTime(sprintf('%d-%02d-%02d', $year, $month, $day));
    }

    /**
     * Format a Nepali date
     */
    public function format(\NepaliDate $date, string $format = '%Y-%m-%d'): string
    {
        return $date->format($format);
    }
}
