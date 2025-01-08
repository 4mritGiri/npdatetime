import csv
import time as _time
import datetime as _actual_datetime

from .config import CALENDAR_PATH, MINDATE, MAXDATE
from .utils import _check_int_field


MINYEAR = MINDATE['year']
MAXYEAR = MAXDATE['year']


_MONTHNAMES = (None, "Bai", "Jes", "Asa", "Shr", "Bha", "Asw", "Kar", "Man", "Pou", "Mag", "Fal", "Cha")
_FULLMONTHNAMES = (None, "Baishakh", "Jestha", "Asar", "Shrawan", "Bhadau", "Aswin", "Kartik", "Mangsir", "Poush", "Magh", "Falgun", "Chaitra")
_MONTHNAMES_NP = (None, "वैशाख", "जेष्ठ", "असार", "श्रावण", "भदौ", "आश्विन", "कार्तिक", "मंसिर", "पौष", "माघ", "फाल्गुण", "चैत्र")

_DAYNAMES = (None, "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
_FULLDAYNAMES = (None, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
_FULLDAYNAMES_NP = (None, "सोमबार", "मंगलबार", "बुधवार", "बिहिबार", "शुक्रबार", "शनिबार", "आइतबार")

_DIGIT_NP = "०१२३४५६७८९"
_EPOCH = _actual_datetime.datetime(1970, 1, 1, tzinfo=_actual_datetime.timezone.utc)

_STRFTIME_CUSTOM_MAP = {
   'a': lambda o: '%s' % _DAYNAMES[(o.weekday() % 7) or 7],
   'A': lambda o: '%s' % _FULLDAYNAMES[(o.weekday() % 7) or 7],
   'G': lambda o: '%s' % _FULLDAYNAMES_NP[(o.weekday() % 7) or 7],
   'w': lambda o: '%d' % o.weekday(),
   'd': lambda o: '%02d' % o.day,
   'D': lambda o: ''.join(_DIGIT_NP[int(i)] for i in '%02d' % o.day),
   'b': lambda o: '%s' % _MONTHNAMES[o.month],
   'B': lambda o: '%s' % _FULLMONTHNAMES[o.month],
   'N': lambda o: '%s' % _MONTHNAMES_NP[o.month],
   'm': lambda o: '%02d' % o.month,
   'n': lambda o: ''.join(_DIGIT_NP[int(i)] for i in '%02d' % o.month),
   'y': lambda o: '%02d' % (o.year % 100),
   'Y': lambda o: '%d' % o.year,
   'k': lambda o: ''.join(_DIGIT_NP[int(i)] for i in '%02d' % (o.year % 100)),
   'K': lambda o: ''.join(_DIGIT_NP[int(i)] for i in '%d' % o.year),
   'H': lambda o: '%02d' % getattr(o, 'hour', 0),
   'h': lambda o: ''.join(_DIGIT_NP[int(i)] for i in '%02d' % getattr(o, 'hour', 0)),
   'I': lambda o: '%02d' % (getattr(o, 'hour', 0) % 12,),
   'i': lambda o: ''.join(_DIGIT_NP[int(i)] for i in '%02d' % (getattr(o, 'hour', 0) % 12,)),
   'p': lambda o: 'AM' if getattr(o, 'hour', 0) < 12 else 'PM',
   'M': lambda o: '%02d' % getattr(o, 'minute', 0),
   'l': lambda o: ''.join(_DIGIT_NP[int(i)] for i in '%02d' % getattr(o, 'minute', 0)),
   'S': lambda o: '%02d' % getattr(o, 'second', 0),
   's': lambda o: ''.join(_DIGIT_NP[int(i)] for i in '%02d' % getattr(o, 'second', 0)),
   'U': lambda o: '%02d' % ((o.timetuple().tm_yday + 7 - o.weekday()) // 7,),
}

_CALENDAR = {}
_DAYS_BEFORE_YEAR = []

with open(CALENDAR_PATH, 'r') as calendar_file:
   file = csv.reader(calendar_file)
   next(file)
   for row in file:
      _CALENDAR[int(row[0])] = [-1, *[sum(int(j) for j in row[1:i]) for i in range(2, 14)]]
      _DAYS_BEFORE_YEAR.append(sum(int(i) for i in row[1:]) + (_DAYS_BEFORE_YEAR[-1] if _DAYS_BEFORE_YEAR else 0))

_MAXORDINAL = _DAYS_BEFORE_YEAR[-1]


def _wrap_strftime(object, format):
   # Don't call utcoffset() or tzname() unless actually needed.
   freplace = None  # the string to use for %f
   zreplace = None  # the string to use for %z
   Zreplace = None  # the string to use for %Z

   # Scan format for %z and %Z escapes, replacing as needed.
   newformat = []
   push = newformat.append
   i, n = 0, len(format)
   while i < n:
      ch = format[i]
      i += 1
      if ch == '%':
         if i < n:
               ch = format[i]
               i += 1
               if ch == 'f':
                  if freplace is None:
                     freplace = '%06d' % getattr(object, 'microsecond', 0)
                  newformat.append(freplace)
               elif ch == 'z':
                  if zreplace is None:
                     zreplace = ""
                     if hasattr(object, "utcoffset"):
                           offset = object.utcoffset()
                           if offset is not None:
                              sign = '+'
                              if offset.days < 0:
                                 offset = -offset
                                 sign = '-'
                              h, m = divmod(offset, _actual_datetime.timedelta(hours=1))
                              assert not m % _actual_datetime.timedelta(minutes=1), "whole minute"
                              m //= _actual_datetime.timedelta(minutes=1)
                              zreplace = '%c%02d%02d' % (sign, h, m)
                  assert '%' not in zreplace
                  newformat.append(zreplace)
               elif ch == 'Z':
                  if Zreplace is None:
                     Zreplace = ""
                     if hasattr(object, "tzname"):
                           s = object.tzname()
                           if s is not None:
                              # strftime is going to have at this: escape %
                              Zreplace = s.replace('%', '%%')
                  newformat.append(Zreplace)
               elif ch in _STRFTIME_CUSTOM_MAP.keys():
                  newformat.append(_STRFTIME_CUSTOM_MAP[ch](object))
               else:
                  push('%')
                  push(ch)
         else:
               push('%')
      else:
         push(ch)
   newformat = "".join(newformat)
   return newformat


def _bin_search(key, *arr):
   index = 0
   while True:
      if len(arr) == 1:
         break
      mid = len(arr) // 2 - 1 + len(arr) % 2
      index += mid
      if key == arr[mid]:
         break
      elif key < arr[mid]:
         index -= mid
         arr = arr[:mid + 1]
      else:
         index += 1
         arr = arr[mid + 1:]
   return index


def _ord2ymd(n):
   year = MINYEAR + _bin_search(n, *_DAYS_BEFORE_YEAR)
   if year > MINYEAR:
      n -= _DAYS_BEFORE_YEAR[year - MINYEAR - 1]
   month = 1 + _bin_search(n, *_CALENDAR[year][1:])
   if month > 1:
      n -= _CALENDAR[year][month - 1]
   return year, month, n


def _days_before_month(year, month):
   """year, month -> number of days in year preceding first day of month."""
   assert 1 <= month <= 12, 'month must be in 1..12'
   if month == 1:
      return 0
   return _CALENDAR[year][month - 1]

def _days_before_year(year):
   """year -> number of days before Baishak 1st of year."""
   assert MINYEAR <= year <= MAXYEAR, "year must be in %s..%s" % (MINYEAR, MAXYEAR)
   if year == MINYEAR:
      return 0
   return _DAYS_BEFORE_YEAR[year - MINYEAR - 1]

def _build_struct_time(y, m, d, hh, mm, ss, dstflag):
   wday = (_ymd2ord(y, m, d) + 5) % 7
   dnum = _days_before_month(y, m) + d
   return _time.struct_time((y, m, d, hh, mm, ss, wday, dnum, dstflag))


def _ymd2ord(year, month, day):
   """year, month, day -> ordinal, considering 1975-Bai-01 as day 1."""
   assert 1 <= month <= 12, 'month must be in 1..12'
   dim = _days_in_month(year, month)
   assert 1 <= day <= dim, ('day must be in 1..%d' % dim)
   return _days_before_year(year) + _days_before_month(year, month) + day



def _days_in_month(year, month):
   assert 1 <= month <= 12, month
   if month == 1:
      return _CALENDAR[year][1]
   return _CALENDAR[year][month] - _CALENDAR[year][month - 1]


def _check_date_fields(year, month, day):
   year = _check_int_field(year)
   month = _check_int_field(month)
   day = _check_int_field(day)
   if not MINYEAR <= year <= MAXYEAR:
      raise ValueError('year must be in %d..%d' % (MINYEAR, MAXYEAR), year)
   if not 1 <= month <= 12:
      raise ValueError('month must be in 1..12', month)
   dim = _days_in_month(year, month)
   if not 1 <= day <= dim:
      raise ValueError('day must be in 1..%d' % dim, day)
   return year, month, day
