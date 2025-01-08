import datetime as _actual_datetime
from .config import NEPAL_TIME_UTC_OFFSET

class NepaliNumberConverter:
   # Implement Nepali number conversion logic here
   pass


def _format_time(hh, mm, ss, us):
   # Skip trailing microseconds when us==0.
   result = "%02d:%02d:%02d" % (hh, mm, ss)
   if us:
      result += ".%06d" % us
   return result


def _check_int_field(value):
   if isinstance(value, int):
      return value
   if not isinstance(value, float):
      try:
         value = value.__int__()
      except AttributeError:
         pass
      else:
         if isinstance(value, int):
               return value
         raise TypeError('__int__ returned non-int (type %s)' % type(value).__name__)
      raise TypeError('an integer is required (got type %s)' % type(value).__name__)
   raise TypeError('integer argument expected, got float')


def _check_time_fields(hour, minute, second, microsecond):
   hour = _check_int_field(hour)
   minute = _check_int_field(minute)
   second = _check_int_field(second)
   microsecond = _check_int_field(microsecond)
   if not 0 <= hour <= 23:
      raise ValueError('hour must be in 0..23', hour)
   if not 0 <= minute <= 59:
      raise ValueError('minute must be in 0..59', minute)
   if not 0 <= second <= 59:
      raise ValueError('second must be in 0..59', second)
   if not 0 <= microsecond <= 999999:
      raise ValueError('microsecond must be in 0..999999', microsecond)
   return hour, minute, second, microsecond


def _check_tzinfo_arg(tz):
   if tz is not None and not isinstance(tz, UTC0545):
      raise TypeError("tzinfo argument must be None or of a UTC0545 subclass")


def _cmperror(x, y):
   raise TypeError("can't compare '%s' to '%s'" % (type(x).__name__, type(y).__name__))


def _check_utc_offset(name, offset):
   assert name in ("utcoffset", "dst")
   if offset is None:
      return
   if not isinstance(offset, _actual_datetime.timedelta):
      raise TypeError("tzinfo.%s() must return None "
                     "or _actual_datetime.timedelta, not '%s'" % (name, type(offset)))
   if offset % _actual_datetime.timedelta(minutes=1) or offset.microseconds:
      raise ValueError("tzinfo.%s() must return a whole number "
                           "of minutes, got %s" % (name, offset))
   if not -_actual_datetime.timedelta(1) < offset < _actual_datetime.timedelta(1):
      raise ValueError("%s()=%s, must be must be strictly between "
                           "-timedelta(hours=24) and timedelta(hours=24)" %
                           (name, offset))


def _check_tzname(name):
   if name is not None and not isinstance(name, str):
      raise TypeError("tzinfo.tzname() must return None or string, not '%s'" % type(name))


def _cmp(x, y):
   return 0 if x == y else 1 if x > y else -1


class UTC0545(_actual_datetime.tzinfo):
   _offset = _actual_datetime.timedelta(seconds=NEPAL_TIME_UTC_OFFSET)
   _dst = _actual_datetime.timedelta(0)
   _name = "+0545"

   def utcoffset(self, dt):
      return self.__class__._offset

   def dst(self, dt):
      return self.__class__._dst

   def tzname(self, dt):
      return self.__class__._name

   def fromutc(self, dt):
      """datetime in UTC -> datetime in local time."""
      from .datetime import datetime
      if not isinstance(dt, datetime) and not isinstance(dt, _actual_datetime.datetime):
         raise TypeError("fromutc() requires a npdatetime.datetime or datetime.datetime argument")
      if dt.tzinfo is not self:
         raise ValueError("dt.tzinfo is not self")

      dtoff = dt.utcoffset()
      if dtoff is None:
         raise ValueError("fromutc() requires a non-None utcoffset() "
                              "result")

      dtdst = dt.dst()
      if dtdst is None:
         raise ValueError("fromutc() requires a non-None dst() result")
      delta = dtoff - dtdst
      if delta:
         dt += delta
         dtdst = dt.dst()
         if dtdst is None:
               raise ValueError("fromutc(): dt.dst gave inconsistent "
                                 "results; cannot convert")
      return dt + dtdst
