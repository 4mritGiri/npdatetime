import sys
import time as _time
import datetime as _actual_datetime
from .config import MINDATE, MAXDATE, REFERENCE_DATE_AD, NEPAL_TIME_UTC_OFFSET

from .core import _FULLMONTHNAMES, _check_date_fields, _actual_datetime, _ord2ymd, MINYEAR, _MAXORDINAL, _days_in_month, _DAYNAMES, _MONTHNAMES, _wrap_strftime, _build_struct_time, _ymd2ord
from .utils import _cmp

class date:
   __slots__ = ('_year', '_month', '_day')

   def __new__(cls, year, month=None, day=None):
      year, month, day = _check_date_fields(year, month, day)
      self = object.__new__(cls)
      self._year = year
      self._month = month
      self._day = day
      return self
   
   def __repr__(self):
      return "%s.%s(%d, %d, %d)" % (
         self.__module__,
         self.__class__.__name__,
         self._year,
         self._month,
         self._day
      )
   
   @classmethod
   def fromtimestamp(cls, t):
      """Construct a date from a POSIX timestamp (like time.time())."""
      y, m, d, hh, mm, ss, weekday, jday, dst = _time.gmtime(t + NEPAL_TIME_UTC_OFFSET)
      return cls.from_datetime_date(_actual_datetime.date(y, m, d))

   @classmethod
   def today(cls):
      """Construct a date from time.time()."""
      t = _time.time()
      return cls.fromtimestamp(t)

   @classmethod
   def fromordinal(cls, n):
      """Construct a date from a (MINYEAR, 1, 1).

      Baishak 1 of year 1975 is day 1.  Only the year, month and day are
      non-zero in the result.
      """
      y, m, d = _ord2ymd(n)
      return cls(y, m, d)

   @classmethod
   def from_datetime_date(cls, from_date):
      """Convert datetime.date to npdatetime.date (A.D date to B.S).

      Parameters
      ----------
      from_date: datetime.date
         The AD date object to be converted.

      Returns
      -------
      npdatetime.date
         The converted npdatetime.date object.
      """
      if not isinstance(from_date, _actual_datetime.date):
         raise TypeError("Unsupported type {}.".format(type(from_date)))
      return cls(MINYEAR, 1, 1) + (from_date - _actual_datetime.date(**REFERENCE_DATE_AD))
   
   def to_datetime_date(self):
      """Convert npdatetime.date to datetime.date (B.S date to A.D).

      Returns
      -------
      datetime.date
         The converted datetime.date object.
      """
      return _actual_datetime.date(**REFERENCE_DATE_AD) + _actual_datetime.timedelta(days=self.toordinal() - 1)

   def calendar(self, month_count=None, justify=4):
      format_str = '{:>%s}' % justify

      def _mark_today(indx, cal, cal_range):
         try:
               # Strip the color codes for comparison
               def remove_color(val):
                  return val.replace('\033[31m', '').replace('\033[32m', '').replace('\033[39m', '').strip()

               indx_day = next(
                  i for i, val in enumerate(cal[indx]) if remove_color(val) == str(self.day)
               )
               # Add a space in front of the "today" text
               cal[indx][indx_day] = '\033[32m{:>{}}\033[39m'.format(remove_color(cal[indx][indx_day]), justify)  # Green for today
         except StopIteration:
               raise ValueError(f"Day {self.day} not found in calendar row {indx}")

      def _mark_saturdays(cal):
         for week in cal[2:]:  # Start from the third row (days start from the third row)
               if len(week) >= 7:  # Ensure full week exists
                  week[6] = '\033[31m{:>{}}\033[39m'.format(week[6].strip(), justify)  # Red for Saturday (7th day)

      # Helper method to generate a single month's calendar
      def _generate_month_calendar(year, month, justify=4):
         total_days_month = _days_in_month(year, month)
         start_weekday = self.__class__(year, month, 1).weekday()
         
         # Instead of using self.strftime('%B %Y'), use the year and month directly
         month_name = _FULLMONTHNAMES[month]  # Assuming _MONTHNAMES is a list of month names
         cal = [[('\033[34m{:^{}}\033[39m'.format(f'{month_name} {year}', (justify + 1) * 7))],
               [format_str.format('Sun'), *(format_str.format(j) for j in _DAYNAMES[1:-2]), '\033[31m{:>{}}\033[39m'.format('Sat', justify)],
               [format_str.format(' ') for _ in range(start_weekday)]]

         cal[-1].extend([format_str.format(j) for j in range(1, 8 - start_weekday)])
         cal_cursor = 8 - start_weekday
         cal_range = [(1, 7 - start_weekday)]

         total_mid_weeks = (total_days_month - cal_cursor) // 7
         for i in range(total_mid_weeks):
            cal_range.append((cal_cursor, cal_cursor + 6))
            cal.append([format_str.format(j) for j in range(cal_cursor, cal_cursor + 7)])
            cal_cursor += 7

         if cal_cursor <= total_days_month:
            cal.append([format_str.format(j) for j in range(cal_cursor, total_days_month + 1)])
            cal_range.append((cal_cursor, total_days_month))

         # Adjust the last row to fill empty spaces for alignment
         if len(cal[-1]) < 7:
            cal[-1].extend([format_str.format(' ')] * (7 - len(cal[-1])))

         if sys.platform.startswith('linux'):
            # Mark the Saturdays in red
            _mark_saturdays(cal)

            # Mark today's date in green
            for i, cr in enumerate(cal_range):
                  if cr[0] <= self.day <= cr[1]:
                     _mark_today(-len(cal_range) + i, cal, cal_range)
                     break

         return '\n' + '\n'.join(' '.join(j) for j in cal) + '\n\n'

      if month_count > 1 and month_count < 13:
         cal_str = ""
         start_month = self.month
         start_year = self.year
         for i in range(month_count):
            current_month = start_month + i
            
            if current_month > 12:
                  current_month -= 12  # Reset month to 1 (January) after December
                  current_year = start_year + 1  # Increment the year when exceeding December
            else:
                  current_year = start_year  # Stay in the same year

            cal_str += _generate_month_calendar(current_year, current_month)

         sys.stdout.write(cal_str)

      else:
         sys.stdout.write(_generate_month_calendar(self.year, self.month))


   def ctime(self):
      """Return ctime() style string."""
      weekday = (self.toordinal() + 5) % 7 or 7
      return "%s %s %2d 00:00:00 %04d" % (_DAYNAMES[weekday], _MONTHNAMES[self._month], self._day, self._year)

   def strftime(self, fmt):
      """Format using strftime()."""
      return _wrap_strftime(self, fmt)

   def __format__(self, fmt):
      if not isinstance(fmt, str):
         raise TypeError("must be str, not %s" % type(fmt).__name__)
      if len(fmt) != 0:
         return self.strftime(fmt)
      return str(self)

   def isoformat(self):
      return "%04d-%02d-%02d" % (self._year, self._month, self._day)

   __str__ = isoformat

   @property
   def year(self):
      """year (1975-2100)"""
      return self._year

   @property
   def month(self):
      """month (1-12)"""
      return self._month

   @property
   def day(self):
      """day (1-32)"""
      return self._day

   def timetuple(self):
      """Return local time tuple compatible with time.localtime()."""
      return _build_struct_time(self._year, self._month, self._day, 0, 0, 0, -1)

   def toordinal(self):
      """Baishak 1 of year 1975 is day 1.  Only the year, month and day values contribute to the result."""
      return _ymd2ord(self._year, self._month, self._day)

   def replace(self, year=None, month=None, day=None):
      """Return a new date with new values for the specified fields."""
      if year is None:
         year = self._year
      if month is None:
         month = self._month
      if day is None:
         day = self._day
      return date(year, month, day)

   def __eq__(self, other):
      if isinstance(other, date):
         return self._cmp(other) == 0
      return NotImplemented

   def __le__(self, other):
      if isinstance(other, date):
         return self._cmp(other) <= 0
      return NotImplemented

   def __lt__(self, other):
      if isinstance(other, date):
         return self._cmp(other) < 0
      return NotImplemented

   def __ge__(self, other):
      if isinstance(other, date):
         return self._cmp(other) >= 0
      return NotImplemented

   def __gt__(self, other):
      if isinstance(other, date):
         return self._cmp(other) > 0
      return NotImplemented

   def _cmp(self, other):
      assert isinstance(other, date)
      y, m, d = self._year, self._month, self._day
      y2, m2, d2 = other._year, other._month, other._day
      return _cmp((y, m, d), (y2, m2, d2))

   def __hash__(self):
      return NotImplemented

   def __add__(self, other):
      """Add two npdatetime.date objects.
      Parameters
      ----------
      other: datetime.timedelta
         The other object added to self.

      Returns
      -------
      npdatetime.date
         The new npdatetime.date object after addition operation.
      """
      if isinstance(other, _actual_datetime.timedelta):
         o = self.toordinal() + other.days
         if 0 < o <= _MAXORDINAL:
               return date.fromordinal(o)
         raise OverflowError("result out of range")
      return NotImplemented

   __radd__ = __add__

   def __sub__(self, other):
      """Subtract two npdatetime.date objects.

      Parameters
      ----------
      other: datetime.timedelta
         The other object to which the self is subtracted from.

      Returns
      -------
      npdatetime.date
         The new npdatetime.date object after subtraction operation.
      """
      if isinstance(other, _actual_datetime.timedelta):
         return self + _actual_datetime.timedelta(-other.days)
      if isinstance(other, date):
         days1 = self.toordinal()
         days2 = other.toordinal()
         return _actual_datetime.timedelta(days1 - days2)
      return NotImplemented

   def weekday(self):
      """Return day of the week, where Sunday == 0 ... Saturday == 6."""
      return (self.toordinal() + 5) % 7

   def isoweekday(self):
      return NotImplemented

   def isocalendar(self):
      return NotImplemented

   def _getstate(self):
      return NotImplemented

   def __setstate(self, string):
      return NotImplemented

   def __reduce__(self):
      return NotImplemented
   
   @classmethod
   def last_day_of_month(cls, year, month):
      """Returns the last day of the given month in the given year."""
      if month == 12:
         next_month = 1
         next_year = year + 1
      else:
         next_month = month + 1
         next_year = year
      
      # The last day of the current month is the first day of the next month minus one day
      next_month_first_day = date(next_year, next_month, 1)
      return (next_month_first_day - _actual_datetime.timedelta(days=1)).day

_date_class = date  # so functions w/ args named "date" can get at the class

date.min = date(**MINDATE)
date.max = date(**MAXDATE)
date.resolution = _actual_datetime.timedelta(days=1)
