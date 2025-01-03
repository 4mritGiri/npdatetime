import npdatetime as npd


class TestInit:
   """Test attributes initialized when a instance of the class is created."""

   def test_max_date_gt_min_date(self):
      assert npd.MAXYEAR > npd.MINYEAR
