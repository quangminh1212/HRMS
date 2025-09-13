import pytest
from datetime import date

from hrms.salary import add_months, months_between


def test_add_months_basic():
    assert add_months(date(2020,1,31), 1) == date(2020,2,29)  # leap year handling
    assert add_months(date(2021,1,31), 1) == date(2021,2,28)
    assert add_months(date(2021,3,31), -1) == date(2021,2,28)


def test_months_between():
    assert months_between(date(2020,1,1), date(2020,2,1)) == 1
    assert months_between(date(2020,1,15), date(2020,2,14)) == 0
    assert months_between(date(2020,1,15), date(2020,2,15)) == 1
