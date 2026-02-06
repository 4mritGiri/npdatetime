"""Test cases for npdatetime Python bindings"""

def test_create_date():
    from npdatetime import NepaliDate
    date = NepaliDate(2077, 5, 19)
    assert date.year == 2077
    assert date.month == 5
    assert date.day == 19

def test_to_gregorian():
    from npdatetime import NepaliDate
    date = NepaliDate(2077, 5, 19)
    year, month, day = date.to_gregorian()
    assert year == 2020
    assert month == 9
    assert day == 4

def test_from_gregorian():
    from npdatetime import NepaliDate
    date = NepaliDate.from_gregorian(2020, 9, 4)
    assert date.year == 2077
    assert date.month == 5
    assert date.day == 19

def test_format():
    from npdatetime import NepaliDate
    date = NepaliDate(2077, 5, 19)
    assert date.format("%Y-%m-%d") == "2077-05-19"
    assert "Bhadra" in date.format("%B")

def test_add_days():
    from npdatetime import NepaliDate
    date = NepaliDate(2077, 5, 19)
    future = date.add_days(10)
    assert future.day == 29

def test_comparison():
    from npdatetime import NepaliDate
    date1 = NepaliDate(2077, 5, 19)
    date2 = NepaliDate(2077, 5, 20)
    assert date1 < date2
    assert date2 > date1
    assert date1 == NepaliDate(2077, 5, 19)

def test_today_conversion():
    from npdatetime import NepaliDate
    from datetime import date
    
    today_ad = date.today()
    nepali_date = NepaliDate.from_gregorian(today_ad.year, today_ad.month, today_ad.day)
    
    # Also verify matches .today()
    assert nepali_date == NepaliDate.today()
    print(f"Today: AD {today_ad} = BS {nepali_date}")

if __name__ == "__main__":
    test_create_date()
    test_to_gregorian()
    test_from_gregorian()
    test_format()
    test_add_days()
    test_comparison()
    test_comparison()
    test_today_conversion()
    print("All Python tests passed!")
