from .core import  _check_date_fields, _time, _actual_datetime,  _build_struct_time, _DAYNAMES,_MONTHNAMES, _MAXORDINAL
from .utils import _format_time, _check_time_fields, _check_tzinfo_arg, _check_tzname, _check_utc_offset, _cmp, _cmperror, UTC0545
import math as _math
from .npdate import date, _date_class


class datetime(date):
   """datetime(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])

   The year, month and day arguments are required. tzinfo may be None, or an
   instance of a tzinfo subclass. The remaining arguments may be ints.
   """
   __slots__ = date.__slots__ + ('_hour', '_minute', '_second', '_microsecond', '_tzinfo', '_hashcode')

   def __new__(cls, year, month=None, day=None, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
      year, month, day = _check_date_fields(year, month, day)
      hour, minute, second, microsecond = _check_time_fields(hour, minute, second, microsecond)
      _check_tzinfo_arg(tzinfo)
      self = object.__new__(cls)
      self._year = year
      self._month = month
      self._day = day
      self._hour = hour
      self._minute = minute
      self._second = second
      self._microsecond = microsecond
      self._tzinfo = UTC0545() if tzinfo is None else tzinfo
      self._hashcode = -1
      return self

   @property
   def hour(self):
      """hour (0-23)"""
      return self._hour

   @property
   def minute(self):
      """minute (0-59)"""
      return self._minute

   @property
   def second(self):
      """second (0-59)"""
      return self._second

   @property
   def microsecond(self):
      """microsecond (0-999999)"""
      return self._microsecond

   @property
   def tzinfo(self):
      """timezone info object"""
      return self._tzinfo

   @classmethod
   def _fromtimestamp(cls, t, utc, tz):
      """Construct a datetime from a POSIX timestamp (like time.time()).

      A timezone info object may be passed in as well.
      """
      frac, t = _math.modf(t)
      us = round(frac * 1e6)
      if us >= 1000000:
         t += 1
         us -= 1000000
      elif us < 0:
         t -= 1
         us += 1000000

      converter = _time.gmtime if utc else _time.localtime
      y, m, d, hh, mm, ss, weekday, jday, dst = converter(t)
      dt = super().from_datetime_date(_actual_datetime.date(y, m, d))
      y, m, d = dt.year, dt.month, dt.day
      ss = min(ss, 59)  # clamp out leap seconds if the platform has them
      return cls(y, m, d, hh, mm, ss, us, tz)

   @classmethod
   def fromtimestamp(cls, t, tz=None):
      """Construct a datetime from a POSIX timestamp (like time.time()).

      A timezone info object may be passed in as well.
      """
      _check_tzinfo_arg(tz)

      result = cls._fromtimestamp(t, tz is not None, tz)
      if tz is not None:
         result = tz.fromutc(result)
      return result

   @classmethod
   def utcfromtimestamp(cls, t):
      """Construct a naive UTC datetime from a POSIX timestamp."""
      return cls._fromtimestamp(t, True, None)

   @classmethod
   def now(cls):
      """Construct a datetime from time.time() and optional time zone info."""
      t = _time.time()
      return cls.fromtimestamp(t, UTC0545())

   @classmethod
   def utcnow(cls):
      """Construct a UTC datetime from time.time()."""
      t = _time.time()
      return cls.utcfromtimestamp(t)

   @classmethod
   def combine(cls, date, time):
      """Construct a datetime from a given date and a given time."""
      if not isinstance(date, _date_class):
         raise TypeError("date argument must be a date instance")
      if not isinstance(time, _actual_datetime.time):
         raise TypeError("time argument must be a time instance")
      return cls(
         date.year, date.month, date.day,
         time.hour, time.minute, time.second, time.microsecond,
         time.tzinfo
      )

   def timetuple(self):
      """Return local time tuple compatible with time.localtime()."""
      dst = self.dst()
      if dst is None:
         dst = -1
      elif dst:
         dst = 1
      else:
         dst = 0
      return _build_struct_time(
         self.year, self.month, self.day,
         self.hour, self.minute, self.second,
         dst
      )

   @classmethod
   def from_datetime_datetime(cls, from_datetime):
      """Convert datetime.date to npdatetime.datetime (A.D datetime to B.S).

      Parameters
      ----------
      from_date: datetime.datetime
         The AD datetime object to be converted.

      Returns
      -------
      npdatetime.datetime
         The converted npdatetime.datetime object.
      """
      from_datetime = from_datetime.astimezone(UTC0545())
      return cls.combine(cls.from_datetime_date(from_datetime.date()), from_datetime.time())

   def to_datetime_datetime(self):
      """Convert npdatetime.datetime to datetime.datetime (B.S datetime to A.D).

      Returns
      -------
      datetime.datetime
         The converted datetime.datetime object.
      """
      return _actual_datetime.datetime.fromtimestamp(self.timestamp())

   def _mktime(self):
      """Return integer POSIX timestamp."""
      max_fold_seconds = 24 * 3600
      t = (self - _EPOCH_BS) // _actual_datetime.timedelta(0, 1)

      def local(u):
         y, m, d, hh, mm, ss = _time.localtime(u)[:6]
         return (datetime(y, m, d, hh, mm, ss) - _EPOCH_BS) // _actual_datetime.timedelta(0, 1)

      # Our goal is to solve t = local(u) for u.
      a = local(t) - t
      u1 = t - a
      t1 = local(u1)
      if t1 == t:
         # We found one solution, but it may not be the one we need.
         # Look for an earlier solution (if `fold` is 0), or a
         # later one (if `fold` is 1).
         u2 = u1 + (-max_fold_seconds, max_fold_seconds)[self.fold]
         b = local(u2) - u2
         if a == b:
               return u1
      else:
         b = t1 - u1
         assert a != b
      u2 = t - b
      t2 = local(u2)
      if t2 == t:
         return u2
      if t1 == t:
         return u1
      # We have found both offsets a and b, but neither t - a nor t - b is
      # a solution.  This means t is in the gap.
      return (max, min)[self.fold](u1, u2)

   def timestamp(self):
      """Return POSIX timestamp as float"""
      if self._tzinfo is None:
         s = self._mktime()
         return s + self.microsecond / 1e6
      else:
         return (self - _EPOCH_BS).total_seconds()

   def utctimetuple(self):
      """Return UTC time tuple compatible with time.gmtime()."""
      offset = self.utcoffset()
      if offset:
         self -= offset
      y, m, d = self.year, self.month, self.day
      hh, mm, ss = self.hour, self.minute, self.second
      return _build_struct_time(y, m, d, hh, mm, ss, 0)

   def date(self):
      """Return the date part."""
      return date(self._year, self._month, self._day)

   def time(self):
      """Return the time part, with tzinfo None."""
      return _actual_datetime.time(self.hour, self.minute, self.second, self.microsecond)

   def timetz(self):
      """Return the time part, with same tzinfo."""
      return _actual_datetime.time(self.hour, self.minute, self.second, self.microsecond, self._tzinfo)

   def replace(self, year=None, month=None, day=None, hour=None,
               minute=None, second=None, microsecond=None, tzinfo=True):
      """Return a new datetime with new values for the specified fields."""
      if year is None:
         year = self.year
      if month is None:
         month = self.month
      if day is None:
         day = self.day
      if hour is None:
         hour = self.hour
      if minute is None:
         minute = self.minute
      if second is None:
         second = self.second
      if microsecond is None:
         microsecond = self.microsecond
      if tzinfo is True:
         tzinfo = self.tzinfo
      return datetime(year, month, day, hour, minute, second, microsecond, tzinfo)

   def astimezone(self, tz=None):
      if tz is None:
         tz = UTC0545()
      elif not isinstance(tz, _actual_datetime.tzinfo):
         raise TypeError("tz argument must be an instance of tzinfo")

      mytz = self.tzinfo
      if mytz is None:
         mytz = self._local_timezone()
         myoffset = mytz.utcoffset(self)
      else:
         myoffset = mytz.utcoffset(self)
         if myoffset is None:
               mytz = self.replace(tzinfo=None)._local_timezone()
               myoffset = mytz.utcoffset(self)

      if tz is mytz:
         return self

      utc = (self - myoffset).replace(tzinfo=tz)

      return tz.fromutc(utc)

   def ctime(self):
      """Return ctime() style string."""
      weekday = (self.toordinal() + 5) % 7 or 7
      return "%s %s %2d %02d:%02d:%02d %04d" % (
         _DAYNAMES[weekday],
         _MONTHNAMES[self._month],
         self._day,
         self._hour, self._minute, self._second,
         self._year
      )

   def isoformat(self, sep='T'):
      """Return the time formatted according to ISO.

      This is 'YYYY-MM-DD HH:MM:SS.mmmmmm', or 'YYYY-MM-DD HH:MM:SS' if
      self.microsecond == 0.

      If self.tzinfo is not None, the UTC offset is also attached, giving
      'YYYY-MM-DD HH:MM:SS.mmmmmm+HH:MM' or 'YYYY-MM-DD HH:MM:SS+HH:MM'.

      Optional argument sep specifies the separator between date and
      time, default 'T'.
      """
      s = (
               "%04d-%02d-%02d%c" % (self._year, self._month, self._day, sep) +
               _format_time(self._hour, self._minute, self._second, self._microsecond)
      )
      off = self.utcoffset()
      if off is not None:
         if off.days < 0:
               sign = "-"
               off = -off
         else:
               sign = "+"
         hh, mm = divmod(off, _actual_datetime.timedelta(hours=1))
         assert not mm % _actual_datetime.timedelta(minutes=1), "whole minute"
         mm //= _actual_datetime.timedelta(minutes=1)
         s += "%s%02d:%02d" % (sign, hh, mm)
      return s

   def __repr__(self):
      """Convert to formal string, for repr()."""
      L = [self._year, self._month, self._day,  # These are never zero
               self._hour, self._minute, self._second, self._microsecond]
      if L[-1] == 0:
         del L[-1]
      if L[-1] == 0:
         del L[-1]
      s = "%s.%s(%s)" % (self.__class__.__module__,
                           self.__class__.__qualname__,
                           ", ".join(map(str, L)))
      if self._tzinfo is not None:
         assert s[-1:] == ")"
         s = s[:-1] + ", tzinfo=%r" % self._tzinfo + ")"
      return s

   def __str__(self):
      """Convert to string, for str()."""
      return self.isoformat(sep=' ')

   @classmethod
   def strptime(cls, date_string, format):
      """string, format -> new datetime parsed from a string (like time.strptime())."""
      from . import _custom_strptime
      return _custom_strptime._strptime_datetime(cls, date_string, format)

   def utcoffset(self):
      """Return the timezone offset in minutes east of UTC (negative west of UTC)."""
      if self._tzinfo is None:
         return None
      offset = self._tzinfo.utcoffset(self)
      _check_utc_offset("utcoffset", offset)
      return offset

   def tzname(self):
      """Return the timezone name.

      Note that the name is 100% informational -- there's no requirement that
      it mean anything in particular. For example, "GMT", "UTC", "-500",
      "-5:00", "EDT", "US/Eastern", "America/New York" are all valid replies.
      """
      if self._tzinfo is None:
         return None
      name = self._tzinfo.tzname(self)
      _check_tzname(name)
      return name

   def dst(self):
      """Return 0 if DST is not in effect, or the DST offset (in minutes
      eastward) if DST is in effect.

      This is purely informational; the DST offset has already been added to
      the UTC offset returned by utcoffset() if applicable, so there's no
      need to consult dst() unless you're interested in displaying the DST
      info.
      """
      if self._tzinfo is None:
         return None
      offset = self._tzinfo.dst(self)
      _check_utc_offset("dst", offset)
      return offset

   def __eq__(self, other):
      if isinstance(other, datetime):
         return self._cmp(other, allow_mixed=True) == 0
      elif not isinstance(other, date):
         return NotImplemented
      else:
         return False

   def __le__(self, other):
      if isinstance(other, datetime):
         return self._cmp(other) <= 0
      elif not isinstance(other, date):
         return NotImplemented
      else:
         _cmperror(self, other)

   def __lt__(self, other):
      if isinstance(other, datetime):
         return self._cmp(other) < 0
      elif not isinstance(other, date):
         return NotImplemented
      else:
         _cmperror(self, other)

   def __ge__(self, other):
      if isinstance(other, datetime):
         return self._cmp(other) >= 0
      elif not isinstance(other, date):
         return NotImplemented
      else:
         _cmperror(self, other)

   def __gt__(self, other):
      if isinstance(other, datetime):
         return self._cmp(other) > 0
      elif not isinstance(other, date):
         return NotImplemented
      else:
         _cmperror(self, other)

   def _cmp(self, other, allow_mixed=False):
      assert isinstance(other, datetime)
      mytz = self._tzinfo
      ottz = other._tzinfo
      myoff = otoff = None

      if mytz is ottz:
         base_compare = True
      else:
         myoff = self.utcoffset()
         otoff = other.utcoffset()
         base_compare = myoff == otoff

      if base_compare:
         return _cmp((self._year, self._month, self._day,
                           self._hour, self._minute, self._second,
                           self._microsecond),
                     (other._year, other._month, other._day,
                           other._hour, other._minute, other._second,
                           other._microsecond))
      if myoff is None or otoff is None:
         if allow_mixed:
               return 2  # arbitrary non-zero value
         else:
               raise TypeError("cannot compare naive and aware datetimes")
      # XXX What follows could be done more efficiently...
      diff = self - other  # this will take offsets into account
      if diff.days < 0:
         return -1
      return diff and 1 or 0

   def __add__(self, other):
      """Add a datetime and a timedelta."""
      if not isinstance(other, _actual_datetime.timedelta):
         return NotImplemented
      delta = _actual_datetime.timedelta(
         self.toordinal(),
         hours=self._hour,
         minutes=self._minute,
         seconds=self._second,
         microseconds=self._microsecond
      )
      delta += other
      hour, rem = divmod(delta.seconds, 3600)
      minute, second = divmod(rem, 60)
      if 0 < delta.days <= _MAXORDINAL:
         return datetime.combine(
               date.fromordinal(delta.days),
               _actual_datetime.time(hour, minute, second, delta.microseconds, tzinfo=self._tzinfo)
         )
      raise OverflowError("result out of range")

   __radd__ = __add__

   def __sub__(self, other):
      """Subtract two datetimes, or a datetime and a timedelta."""
      if not isinstance(other, datetime):
         if isinstance(other, _actual_datetime.timedelta):
               return self + -other
         return NotImplemented

      days1 = self.toordinal()
      days2 = other.toordinal()
      secs1 = self._second + self._minute * 60 + self._hour * 3600
      secs2 = other._second + other._minute * 60 + other._hour * 3600
      base = _actual_datetime.timedelta(days1 - days2, secs1 - secs2, self._microsecond - other._microsecond)
      if self._tzinfo is other._tzinfo:
         return base
      myoff = self.utcoffset()
      otoff = other.utcoffset()
      if myoff == otoff:
         return base
      if myoff is None or otoff is None:
         raise TypeError("cannot mix naive and timezone-aware time")
      return base + otoff - myoff

   def __hash__(self):
      return NotImplemented

   def _getstate(self):
      return NotImplemented

   def __setstate(self, string, tzinfo):
      return NotImplemented

   def __reduce__(self):
      return NotImplemented


datetime.min = datetime(1975, 1, 1)
datetime.max = datetime(2100, 12, 30, 23, 59, 59, 999999)
datetime.resolution = _actual_datetime.timedelta(microseconds=1)

_EPOCH_BS = datetime.from_datetime_datetime(_actual_datetime.datetime(1970, 1, 1, tzinfo=_actual_datetime.timezone.utc))