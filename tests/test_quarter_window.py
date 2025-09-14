from datetime import date

def test_quarter_window_basic():
    from hrms.app import quarter_window
    # 2025-05-10 is in Q2 (Apr-Jun)
    s, e = quarter_window(date(2025,5,10))
    assert s == date(2025,4,1)
    assert e == date(2025,6,30)
