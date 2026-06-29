"""
Unit tests for normaliser.py
"""

import pytest
from src.etl.normaliser import normalize_year, normalize_ticker


# -----------------------------
# normalize_year() Tests (20)
# -----------------------------

@pytest.mark.parametrize(
    "input_year, expected",
    [
        ("2024", 2024),
        ("2023", 2023),
        ("2022", 2022),
        ("2021", 2021),
        ("2020", 2020),
        (2024, 2024),
        (2023, 2023),
        (2022, 2022),
        (2021, 2021),
        (2020, 2020),
        (" 2024 ", 2024),
        ("2019", 2019),
        ("2018", 2018),
        ("2017", 2017),
        ("2016", 2016),
        ("2015", 2015),
        ("2014", 2014),
        ("2013", 2013),
        ("2012", 2012),
        ("2011", 2011),
    ]
)
def test_normalize_year(input_year, expected):
    assert normalize_year(input_year) == expected


# -----------------------------
# normalize_ticker() Tests (15)
# -----------------------------

@pytest.mark.parametrize(
    "ticker, expected",
    [
        ("tcs", "TCS"),
        ("infy", "INFY"),
        ("hdfcbank", "HDFCBANK"),
        ("reliance", "RELIANCE"),
        ("lt", "LT"),
        (" tcs ", "TCS"),
        (" infy ", "INFY"),
        ("AxisBank", "AXISBANK"),
        ("sbin", "SBIN"),
        ("itc", "ITC"),
        ("asianpaint", "ASIANPAINT"),
        ("bajajfin", "BAJAJFIN"),
        ("maruti", "MARUTI"),
        ("nestle", "NESTLE"),
        ("tatamotors", "TATAMOTORS"),
    ]
)
def test_normalize_ticker(ticker, expected):
    assert normalize_ticker(ticker) == expected