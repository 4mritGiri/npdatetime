import npdatetime


class TestStrftime:

   def test_strftime_date(self):
      dt = npdatetime.date(2077, 6, 4)
      assert dt.strftime("%m/%d/%Y") == "06/04/2077"
      assert dt.strftime("%A of %B %d %y") == "Sunday of Aswin 04 77"
      assert dt.strftime("%a %b") == "Sun Asw"

      dt = npdatetime.date(2077, 2, 32)
      assert dt.strftime("%d-%m-%Y") == "32-02-2077"

   def test_strftime_datetime(self):
      dt = npdatetime.datetime(2052, 10, 29, 15, 22, 50, 2222)
      assert dt.strftime("%m/%d/%Y %I:%M:%S.%f %p %a %A %U") == "10/29/2052 03:22:50.002222 PM Mon Monday 44"


class TestStrptime:

   def test_strptime_date(self):
      assert npdatetime.datetime.strptime("2011-10-11", "%Y-%m-%d").date() == npdatetime.date(2011, 10, 11)
      assert npdatetime.datetime.strptime("2077-02-32", "%Y-%m-%d").date() == npdatetime.date(2077, 2, 32)

   def test_strptime_datetime(self):
      assert npdatetime.datetime.strptime("Asar 23 2025 10:00:00",
                                                "%B %d %Y %H:%M:%S") == npdatetime.datetime(2025, 3, 23, 10, 0, 0)

   def test_strptime_year_special_case(self):
      assert npdatetime.datetime.strptime("89", "%y") == npdatetime.datetime(2089, 1, 1)
      assert npdatetime.datetime.strptime("90", "%y") == npdatetime.datetime(1990, 1, 1)
      assert npdatetime.datetime.strptime("00", "%y") == npdatetime.datetime(2000, 1, 1)