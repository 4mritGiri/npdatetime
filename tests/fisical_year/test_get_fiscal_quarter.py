import unittest
from npdatetime import date
from npdatetime.fiscal_year import get_fiscal_quarter


class TestGetFiscalQuarter(unittest.TestCase):
   def test_quarter_1(self):
      self.assertEqual(get_fiscal_quarter(date(2080, 4, 1)), 1)
      self.assertEqual(get_fiscal_quarter(date(2080, 6, 30)), 1)  # Adjusted logic if needed

   def test_quarter_2(self):
      self.assertEqual(get_fiscal_quarter(date(2080, 7, 1)), 2)
      self.assertEqual(get_fiscal_quarter(date(2080, 9, 29)), 2)  # Valid day

   def test_quarter_3(self):
      self.assertEqual(get_fiscal_quarter(date(2080, 10, 1)), 3)
      self.assertEqual(get_fiscal_quarter(date(2080, 12, 30)), 3)

   def test_quarter_4(self):
      self.assertEqual(get_fiscal_quarter(date(2080, 1, 1)), 4)
      self.assertEqual(get_fiscal_quarter(date(2080, 3, 30)), 4)


if __name__ == "__main__":
   unittest.main()
